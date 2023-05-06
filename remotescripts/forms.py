from functools import lru_cache
from django import forms
from django.http import QueryDict
from django.core.validators import integer_validator
from remotescripts.models import (
    ScriptConfigurationBase,
    RemoteScriptConfiguration,
    ScriptArgumentBase,
    ScriptPositionalArgument,
    ScriptKeywordArgument,
    ScriptOutputFile,
)
from remotescripts.utilities import split_with_spaces_commas
from remotescripts.validators import string_validator, choice_validator


class ScriptExecutionForm(forms.ModelForm):
    # Map type of argument to appropriate form field.
    ARG_TO_FIELD_MAP = {
        ScriptArgumentBase.ARGUMENT_INT: forms.IntegerField,
        ScriptArgumentBase.ARGUMENT_STR: forms.CharField,
        ScriptArgumentBase.ARGUMENT_CHO: forms.ChoiceField,
    }

    # Map type of argument to specific validators, can be extended as needed.
    ARG_TO_VALIDATOR_MAP = {
        ScriptArgumentBase.ARGUMENT_INT: [integer_validator],
        ScriptArgumentBase.ARGUMENT_STR: [string_validator],
        ScriptArgumentBase.ARGUMENT_CHO: [choice_validator],
    }

    POSITIONAL_FIELD_NAME_PREFIX = "pos"

    def __init__(self, *args, **kwargs):
        """
        Prepares a form to display to the user to run a command, by dynamically adding fields
        for each type of argument. Arguments are added by the admin in the Database.
        """
        super().__init__(*args, **kwargs)
        i = 0
        # Add positional arguments to the form
        for arg in ScriptPositionalArgument.objects.filter(
            mother_script=self.instance
        ).order_by("position"):
            field_name = (
                arg.name if arg.name else f"{self.POSITIONAL_FIELD_NAME_PREFIX}{i}"
            )
            self.fields[field_name] = self.ARG_TO_FIELD_MAP[arg.type](
                validators=[
                    *self.ARG_TO_VALIDATOR_MAP[arg.type]
                ]  # Add validators specific to the type of argument
            )
            self.fields[field_name].widget.attrs["class"] = "form-control"
            self.fields[field_name].widget.attrs["placeholder"] = (
                arg.help_text if arg.help_text else ""
            )
            if arg.type == ScriptArgumentBase.ARGUMENT_CHO:
                self.fields[field_name].widget.attrs["class"] += " custom-select"
                values = split_with_spaces_commas(arg.valid_choices)
                self.fields[field_name].choices = [(v, v) for v in values]

            if arg.default_value:
                self.fields[field_name].initial = arg.default_value
            i += 1  # Count position of the argument

        # Add keyword arguments. They are added after the positional ones.
        for kwarg in ScriptKeywordArgument.objects.filter(mother_script=self.instance):
            field_name = kwarg.name if kwarg.name else kwarg.keyword
            self.fields[field_name] = self.ARG_TO_FIELD_MAP[kwarg.type](
                validators=[
                    *self.ARG_TO_VALIDATOR_MAP[arg.type]
                ]  # Add validators specific to the type of argument
            )
            self.fields[field_name].widget.attrs["class"] = "form-control"
            self.fields[field_name].widget.attrs["placeholder"] = (
                kwarg.help_text if kwarg.help_text else ""
            )
            if kwarg.type == ScriptArgumentBase.ARGUMENT_CHO:
                self.fields[field_name].widget.attrs["class"] += " custom-select"
                values = split_with_spaces_commas(kwarg.valid_choices)
                self.fields[field_name].choices = [(v, v) for v in values]
            if kwarg.default_value:
                self.fields[field_name].initial = kwarg.default_value

    class Meta:
        model = ScriptConfigurationBase
        fields = []

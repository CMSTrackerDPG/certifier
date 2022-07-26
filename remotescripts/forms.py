from functools import lru_cache
from django import forms
from django.http import QueryDict
from remotescripts.models import (
    ScriptConfigurationBase,
    RemoteScriptConfiguration,
    ScriptArgumentBase,
    ScriptPositionalArgument,
    ScriptKeywordArgument,
    ScriptOutputFile,
)
from remotescripts.utilities import split_with_spaces_commas


class ScriptExecutionForm(forms.ModelForm):
    ARG_TO_FIELD_MAP = {
        ScriptArgumentBase.ARGUMENT_INT: forms.IntegerField,
        ScriptArgumentBase.ARGUMENT_STR: forms.CharField,
        ScriptArgumentBase.ARGUMENT_CHO: forms.ChoiceField,
    }

    POSITIONAL_FIELD_NAME_PREFIX = "pos"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        i = 0
        # Add positional arguments
        for arg in ScriptPositionalArgument.objects.filter(
            mother_script=self.instance
        ).order_by("position"):
            field_name = (
                arg.name if arg.name else f"{self.POSITIONAL_FIELD_NAME_PREFIX}{i}"
            )
            self.fields[field_name] = self.ARG_TO_FIELD_MAP[arg.type]()
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
            i += 1

        # Add keyword arguments
        for kwarg in ScriptKeywordArgument.objects.filter(mother_script=self.instance):
            field_name = kwarg.name if kwarg.name else kwarg.keyword
            self.fields[field_name] = self.ARG_TO_FIELD_MAP[kwarg.type]()
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

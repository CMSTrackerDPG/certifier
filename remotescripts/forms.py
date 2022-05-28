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


class ScriptExecutionForm(forms.ModelForm):
    ARG_TO_FIELD_MAP = {
        ScriptArgumentBase.ARGUMENT_INT: forms.IntegerField,
        ScriptArgumentBase.ARGUMENT_STR: forms.CharField,
    }

    POSITIONAL_FIELD_NAME_PREFIX = "pos"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        i = 0
        # Add positional arguments
        for arg in ScriptPositionalArgument.objects.filter(mother_script=self.instance):
            field_name = (
                arg.name if arg.name else f"{self.POSITIONAL_FIELD_NAME_PREFIX}{i}"
            )
            self.fields[field_name] = self.ARG_TO_FIELD_MAP[arg.type]()

            i += 1

        # Add keyword arguments
        for kwarg in ScriptKeywordArgument.objects.filter(mother_script=self.instance):
            field_name = kwarg.name if kwarg.name else kwarg.keyword
            self.fields[field_name] = self.ARG_TO_FIELD_MAP[kwarg.type]()

    class Meta:
        model = ScriptConfigurationBase
        fields = []

from django import forms
from remotescripts.models import (
    ScriptConfigurationBase,
    RemoteScriptConfiguration,
    ScriptArgumentBase,
    ScriptPositionalArgument,
    ScriptKeywordArgument,
    ScriptOutputFile,
)


class ScriptExecutionForm(forms.Form):
    ARG_TO_FIELD_MAP = {
        ScriptArgumentBase.ARGUMENT_INT: forms.IntegerField,
        ScriptArgumentBase.ARGUMENT_STR: forms.CharField,
    }

    POSITIONAL_FIELD_NAME_PREFIX = "pos"

    @classmethod
    def generate_form(
        cls, config_instance: ScriptConfigurationBase, init_data: dict = None
    ):
        form = cls
        i = 0

        for arg in config_instance.positional_arguments.all():
            field_name = f"{cls.POSITIONAL_FIELD_NAME_PREFIX}{i}"
            form.base_fields[field_name] = cls.ARG_TO_FIELD_MAP[arg.type]()
            i += 1

        for kwarg in config_instance.keyword_arguments.all():
            field_name = kwarg.keyword
            form.base_fields[field_name] = cls.ARG_TO_FIELD_MAP[kwarg.type]()
        return form

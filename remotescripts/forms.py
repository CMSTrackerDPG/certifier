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
    def generate_form(cls, config_instance: ScriptConfigurationBase):
        """
        Create a ScriptExecutionForm dynamically, adding positional
        and keyword arguments to it, based on the ScriptPositionalArgument and
        ScriptKeywordArgument entries connected to the ScriptConfigurationBase
        instance.
        """
        form = cls
        i = 0
        # Add positional arguments
        for arg in config_instance.positional_arguments.all():
            field_name = f"{cls.POSITIONAL_FIELD_NAME_PREFIX}{i}"
            form.base_fields[field_name] = cls.ARG_TO_FIELD_MAP[arg.type]()
            i += 1

        # Add keyword arguments
        for kwarg in config_instance.keyword_arguments.all():
            field_name = kwarg.keyword
            form.base_fields[field_name] = cls.ARG_TO_FIELD_MAP[kwarg.type]()
        return form

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

    @classmethod
    def generate_form(
        cls, config_instance: ScriptConfigurationBase, init_data: dict = None
    ):
        form = cls
        print(dir(form))
        i = 0

        print(config_instance.positional_arguments)

        for arg in config_instance.positional_arguments.all():
            field_name = f"pos{i}"
            form.base_fields[field_name] = cls.ARG_TO_FIELD_MAP[arg.type]()
            # form.initial[field_name] = ""
            i += 1

        for kwarg in config_instance.keyword_arguments.all():
            field_name = kwarg.keyword
            form.base_fields[field_name] = cls.ARG_TO_FIELD_MAP[kwarg.type]()
            # form.initial[field_name] = ""
        return form

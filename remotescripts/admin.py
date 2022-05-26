from django.contrib import admin
from remotescripts.models import (
    BashScriptConfiguration,
    ScriptKeywordArgument,
    ScriptPositionalArgument,
    ScriptOutputFile,
    RemoteScriptConfiguration,
)

admin.site.register(BashScriptConfiguration)
admin.site.register(ScriptKeywordArgument)
admin.site.register(ScriptPositionalArgument)
admin.site.register(ScriptOutputFile)
admin.site.register(RemoteScriptConfiguration)

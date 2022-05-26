from django.contrib import admin
from remotescripts.models import (
    ScriptConfigurationBase,
    BashScriptConfiguration,
    ScriptKeywordArgument,
    ScriptPositionalArgument,
    ScriptOutputFile,
    RemoteScriptConfiguration,
)

admin.site.register(BashScriptConfiguration)
admin.site.register(RemoteScriptConfiguration)


@admin.register(ScriptKeywordArgument)
class ScriptKeywordArgumentAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "mother_script":
            kwargs["queryset"] = ScriptConfigurationBase.objects.select_subclasses()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ScriptPositionalArgument)
class ScriptPositionalArgumentAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "mother_script":
            kwargs["queryset"] = ScriptConfigurationBase.objects.select_subclasses()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ScriptOutputFile)
class ScriptOutputFileAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "mother_script":
            kwargs["queryset"] = ScriptConfigurationBase.objects.select_subclasses()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

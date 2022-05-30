import logging
from django.contrib import admin
from remotescripts.models import (
    ScriptConfigurationBase,
    BashScriptConfiguration,
    ScriptKeywordArgument,
    ScriptPositionalArgument,
    ScriptOutputFile,
    RemoteScriptConfiguration,
)

logger = logging.getLogger(__name__)

admin.site.register(BashScriptConfiguration)


@admin.action(description="Execute this script")
def execute(modeladmin, request, queryset):
    for s in queryset:
        logger.info(f"Executing {str(s)}")
        s.execute()


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


@admin.register(RemoteScriptConfiguration)
class RemoteScriptConfigurationAdmin(admin.ModelAdmin):
    list_display = ("title", "num_pos_args", "num_kw_args", "num_output_files")
    actions = [execute]

    def num_pos_args(self, obj):
        return obj.positional_arguments.count()

    def num_kw_args(self, obj):
        return obj.keyword_arguments.count()

    def num_output_files(self, obj):
        return obj.output_files.count()

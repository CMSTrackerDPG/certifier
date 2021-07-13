from django.contrib import admin

# Register your models here.
from checklists.models import Checklist, ChecklistItem, ChecklistItemGroup

admin.site.register(Checklist)
admin.site.register(ChecklistItem)
admin.site.register(ChecklistItemGroup)
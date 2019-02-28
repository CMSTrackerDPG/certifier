from django.contrib import admin

# Register your models here.
from oms.models import OmsRun, OmsFill

admin.site.register(OmsRun)
admin.site.register(OmsFill)
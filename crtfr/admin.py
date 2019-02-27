from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, RunCertification, RunReconstruction, \
    TrackingProblem, StripProblem, PixelProblem, BadReason

admin.site.register(User, UserAdmin)
admin.site.register(RunReconstruction)
admin.site.register(RunCertification)
admin.site.register(BadReason)
admin.site.register(PixelProblem)
admin.site.register(StripProblem)
admin.site.register(TrackingProblem)


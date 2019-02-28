from django.contrib import admin

from .models import (
    TrackerCertification,
    RunReconstruction,
    TrackingProblem,
    StripProblem,
    PixelProblem,
    BadReason,
)

admin.site.register(RunReconstruction)
admin.site.register(TrackerCertification)
admin.site.register(BadReason)
admin.site.register(PixelProblem)
admin.site.register(StripProblem)
admin.site.register(TrackingProblem)

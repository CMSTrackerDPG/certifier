from shiftleader.utilities.utilities import DateConverter
from django.urls import path, register_converter

from . import views


register_converter(DateConverter, "yyyy")
app_name = "shiftleader"

urlpatterns = [
    path("", views.shiftleader_view, name="shiftleader"),
    path(
        "generate_presentation/<yyyy:date_from>/<yyyy:date_to>/",
        views.ShiftLeaderReportPresentationView.as_view(),
        name="generate_presentation",
    ),
]

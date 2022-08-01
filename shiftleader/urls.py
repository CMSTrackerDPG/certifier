from datetime import datetime
from django.urls import path, register_converter

from . import views


class DateConverter:
    regex = "\d{4}-\d{2}-\d{2}"

    def to_python(self, value):
        return datetime.strptime(value, "%Y-%m-%d").date()

    def to_url(self, value):
        return value


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

from django.urls import path

from . import views

app_name = "shiftleader"

urlpatterns = [
    path("", views.shiftleader_view, name="shiftleader"),
    path(
        "generate_presentation/<int:week_number>/",
        views.ShiftLeaderReportPresentationView.as_view(),
        name="generate_presentation",
    ),
]

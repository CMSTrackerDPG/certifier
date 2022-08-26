from django.urls import path

from . import views

app_name = "summary"

urlpatterns = [
    path("", views.summaryView, name="summary"),
    path("summary_info/", views.SummaryExtraInfoView.as_view(), name="summary_info"),
]

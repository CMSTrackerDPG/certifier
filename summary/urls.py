from django.urls import path

from . import views

app_name = "summary"

urlpatterns = [
    path("", views.SummaryView.as_view(), name="summary"),
]

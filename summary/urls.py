from django.urls import path

from . import views

app_name = "summary"

urlpatterns = [
    path("", views.summaryView, name="summary"),
    # path("extra_links/", views.extra_
]

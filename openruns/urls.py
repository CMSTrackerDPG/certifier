from django.urls import include, path
from . import views

app_name = "openruns"

urlpatterns = [
    path("", views.openruns, name="openruns"),
]


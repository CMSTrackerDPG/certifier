from django.urls import include, path
from . import views

app_name = "trackermaps"
urlpatterns = [
    path("", views.maps, name="maps"),
]

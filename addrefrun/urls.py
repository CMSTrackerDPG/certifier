from django.urls import path

from . import views

app_name = "addrefrun"
urlpatterns = [
    path("", views.addreference, name="addrefrun"),
    path("update_refruns_info/", views.update_refruns_info, name="update_refruns_info"),
]

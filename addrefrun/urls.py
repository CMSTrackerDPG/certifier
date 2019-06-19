from django.urls import path

from . import views

app_name='addrefrun'
urlpatterns = [
    path("", views.addreference, name="addrefrun"),
]

from django.urls import include, path
from . import views

app_name = "listruns"
urlpatterns = [
    path("", views.listruns, name="list"),
]

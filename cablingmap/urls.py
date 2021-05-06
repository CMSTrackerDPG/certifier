from django.urls import path
from cablingmap import views

app_name = "cablingmap"
urlpatterns = [
    path("", views.cablingmapHome, name = "cablingmapHome"),
]

from django.urls import path
from mlplayground import views

urlpatterns = [
    path("", views.mlplayground),
]

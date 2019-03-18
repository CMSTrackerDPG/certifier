from django.urls import path

from . import views

urlpatterns = [
    path("api/data/", views.ChartData.as_view()),
]

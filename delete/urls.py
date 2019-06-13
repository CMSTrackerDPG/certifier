from django.urls import path

from . import views

app_name = "delete"

urlpatterns = [
    path("<int:pk>/<int:run_number>/<reco>/", views.DeleteRun.as_view(), name="delete"),
    path("hard/<int:pk>/<int:run_number>/<reco>/", views.hard_delete_run_view, name="hard_delete_run"),
]

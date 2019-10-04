from django.urls import path

from . import views

app_name = "delete"

urlpatterns = [
    path("<int:pk>/<int:run_number>/<reco>/", views.DeleteRun.as_view(), name="delete"),
    path("hard/<int:pk>/<int:run_number>/<reco>/", views.hard_delete_run_view, name="hard_delete_run"),
    path("delete/<int:run_number>/<reco>/", views.hard_delete_reference_run, name="delete_reference"),
    path("delete/<int:run_number>/", views.hard_delete_open_run, name="delete_open_run"),
]

from django.urls import path

from . import views

app_name = "restore"

urlpatterns = [
    path("<int:pk>/<int:run_number>/<reco>/", views.restore_run_view, name="restore_run"),
]

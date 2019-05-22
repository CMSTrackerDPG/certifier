from django.urls import path

from . import views

app_name = "shiftleader"

urlpatterns = [
    path("", views.shiftleader_view, name="shiftleader"),
    path("summary/", views.summaryView, name="summary"),
    path("<int:pk>/delete/<int:run_number>/<reco>/", views.DeleteRun.as_view(), name="delete"),
    path("<int:pk>/restore_run/<int:run_number>/<reco>/", views.restore_run_view, name="restore_run"),
    path("<int:pk>/hard_delete_run/<int:run_number>/<reco>/", views.hard_delete_run_view, name="hard_delete_run"),
]

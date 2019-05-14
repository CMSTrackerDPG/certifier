from django.urls import path

from . import views

app_name = "shiftleader"

urlpatterns = [
    path("", views.shiftleader_view, name="shiftleader"),
    path("<int:pk>/delete/<int:run_number>/<reco>/", views.DeleteRun.as_view(), name="delete"),
]

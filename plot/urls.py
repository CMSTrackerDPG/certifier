
from django.urls import path

from . import views

urlpatterns = [
    path("<int:run_number>/<reco>/", views.plot, name="plot"),
]

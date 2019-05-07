from django.urls import include, path

from . import views

urlpatterns = [
    path("<int:run_number>/<reco>/", views.certify, name="certify"),
    path("createdataset/", views.createDataset, name='createdataset'),
]

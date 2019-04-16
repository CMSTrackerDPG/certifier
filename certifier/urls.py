from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:run_number>/<reco>/", views.certify, name="certify"),
    path("createdataset/", views.createDataset, name='createdataset'),
]

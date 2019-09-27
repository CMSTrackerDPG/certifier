from django.urls import include, path

from . import views

urlpatterns = [
    path("<int:run_number>/", views.certify, name="certify"),
    path("createdataset/", views.createDataset, name='createdataset'),
    path("addbadreason/", views.addBadReason, name='addbadreason'),
]

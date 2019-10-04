from django.urls import include, path, re_path

from . import views

urlpatterns = [
    re_path("<int:run_number>/(?P<dataset>.+)/$", views.certify, name="certify"),
    path("<int:run_number>/", views.certify, name="certify"),
    path("createdataset/", views.createDataset, name='createdataset'),
    path("addbadreason/", views.addBadReason, name='addbadreason'),
]

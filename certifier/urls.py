from django.urls import include, path, re_path

from . import views

urlpatterns = [
    re_path("<int:run_number>/(?P<dataset>.+)/$", views.certify, name="certify"),
    path("<int:run_number>/", views.certify, name="certify"),
    path("<int:run_number>/<reco>/", views.certify, name="certify"),
    path("promote/<int:run_number>/<reco>/", views.promoteToReference, name='promote'),
    path("addbadreason/", views.addBadReason, name='addbadreason'),
]

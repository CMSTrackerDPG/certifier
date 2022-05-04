from django.urls import include, path, re_path
from certifier import views

urlpatterns = [
    re_path("<int:run_number>/(?P<dataset>.+)/$", views.certify, name="certify"),
    path("<int:run_number>/", views.certify, name="certify"),
    path("<int:run_number>/<reconstruction_type>/", views.certify, name="certify"),
    path(
        "promote/<int:run_number>/<reconstruction_type>/",
        views.promoteToReference,
        name="promote",
    ),
    path("addbadreason/", views.addBadReason, name="addbadreason"),
    path("allRunsRefRuns/", views.runRefRun_list),
]

from django.urls import include, path, re_path
from certifier import views

urlpatterns = [
    # re_path("<int:run_number>/(?P<dataset>.+)/$", views.certify, name="certify"),
    # path("<int:run_number>/", views.certify, name="certify"),
    # path("<int:run_number>/<reco>/", views.certify, name="certify"),
    re_path(
        "<int:run_number>/(?P<dataset>.+)/$",
        views.CertifyView.as_view(),
        name="certify",
    ),
    path("<int:run_number>/", views.CertifyView.as_view(), name="certify"),
    path("<int:run_number>/<reco>/", views.CertifyView.as_view(), name="certify"),
    path(
        "promote/<int:run_number>/<reco>/",
        views.promoteToReference,
        name="promote",
    ),
    path("badreasons/", views.badReason, name="badreasons"),
    path("addbadreasonform/", views.addBadReasonForm, name="addbadreasonform"),
    path("allRunsRefRuns/", views.runRefRun_list),
]

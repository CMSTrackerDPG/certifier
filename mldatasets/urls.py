from django.urls import path
from mldatasets import views

urlpatterns = [
    path("allRunsRefRuns/", views.runRefRun_list)
    # path("allRuns/", views.run_list)
]
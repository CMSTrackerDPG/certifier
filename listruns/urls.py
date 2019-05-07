from django.urls import include, path
from . import views

app_name = "listruns"
urlpatterns = [
    path("", views.listruns, name="list"),
    path("<int:pk>/update/<int:run_number>/<reco>/", views.UpdateRun.as_view(), name="update"),
]

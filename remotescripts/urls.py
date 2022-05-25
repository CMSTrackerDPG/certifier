from django.urls import include, path, re_path
from remotescripts import views

app_name = "remotescripts"
urlpatterns = [
    path("trackermaps", views.TrackerMapsView.as_view(), name="trackermaps"),
]

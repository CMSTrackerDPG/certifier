from django.urls import include, path, re_path
from remotescripts import views

app_name = "remotescripts"
urlpatterns = [
    path("trackermaps", views.TrackerMapsView.as_view(), name="trackermaps"),
    path("all", views.AllRemoteScriptsView.as_view(), name="all"),
    path("remote/<int:pk>/", views.RemoteScriptView.as_view(), name="remote"),
]

from django.urls import include, path, re_path
from remotescripts import views

app_name = "remotescripts"
urlpatterns = [
    path("remote/list/", views.RemoteScriptListView.as_view(), name="list"),
    path("remote/<int:pk>/", views.RemoteScriptView.as_view(), name="detail"),
]

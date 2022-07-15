from django.urls import include, path, re_path
from oms import views

urlpatterns = [
    path(
        "update_run/<int:pk>/",
        views.OmsRunUpdateView.as_view(),
        name="update_run",
    )
]

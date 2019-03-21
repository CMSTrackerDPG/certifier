from django.urls import path

from . import views

app_name='users'
urlpatterns = [
    path("logout/", views.logout_view, name="logout"),
    path("logout-status/", views.logout_status, name="logout_status"),
]

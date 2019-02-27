from django.urls import path

from . import views

urlpatterns = [
    path('api/oms/run/<int:run_number>/', views.run, name='run'),
    path('api/oms/fill/<int:fill_number>/', views.fill, name='run'),
]
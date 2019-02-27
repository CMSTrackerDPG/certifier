from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('certify/<int:run_number>/<reco>/', views.certify, name='certify'),
    path('analyse/<int:run_number>/<reco>/', views.analyse, name='analyse'),
    path('plot/<int:run_number>/<reco>/', views.plot, name='plot'),
]
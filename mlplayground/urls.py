from django.urls import path
from mlplayground import views

app_name = "mlpayground"
urlpatterns = [
    path("", views.mlplayground, name="mlplaygroundHome"),
]

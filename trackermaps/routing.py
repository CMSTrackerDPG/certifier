from django.urls import path

from . import output_socket

websocket_urlpatterns = [
    path('ws/output/', output_socket.OutputSocket),
]

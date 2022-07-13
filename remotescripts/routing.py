from django.urls import path, re_path

from . import output_socket, consumers

websocket_urlpatterns = [
    path("ws/output/", output_socket.OutputSocket.as_asgi()),
    re_path(
        r"ws/remotescripts/(?P<script_id>\d+)/$",
        consumers.ScriptOutputConsumer.as_asgi(),
    ),
]

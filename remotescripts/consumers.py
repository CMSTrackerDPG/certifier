import logging
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

logger = logging.getLogger(__name__)


class ScriptOutputConsumer(WebsocketConsumer):
    def connect(self):
        """Runs on websocket connected"""
        self.script_id = self.scope["url_route"]["kwargs"]["script_id"]
        self.group_name = f"output_{self.script_id}"

        # Join group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()
        logger.debug(f"Client {self.channel_name} connected to {self.group_name}")

    def disconnect(self, code):
        """Leave group"""
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        logger.debug(f"Client {self.channel_name} disconnected from {self.group_name}")

    # # Receive message from WebSocket
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json["message"]

    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.group_name, {"type": "chat_message", "message": message}
    #     )

    def script_output(self, event):
        """Receive message from group"""
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

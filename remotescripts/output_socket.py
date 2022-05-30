from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class OutputSocket(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("output_group", self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("output_group", self.channel_name)

    # Receive message from the group
    def channel_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

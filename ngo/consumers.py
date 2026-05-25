import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class NGONotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'ngo_notifications'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from room group
    def ngo_notification(self, event):
        message = event['message']
        restaurant_name = event['restaurant_name']
        quantity = event['quantity']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'restaurant_name': restaurant_name,
            'quantity': quantity
        }))

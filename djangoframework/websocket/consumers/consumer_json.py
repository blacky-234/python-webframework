from channels.generic.websocket import AsyncJsonWebsocketConsumer,AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse

class AuthenticatedChatRoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            raise DenyConnection("Login required")

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content):
        user = self.scope["user"]
        message = content.get('message')

        # Broadcast message with username to the group
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat.message',
            'user': user.username,
            'message': message,
        })

    async def chat_message(self, event):
        await self.send_json({
            'user': event['user'],
            'message': event['message'],
        })


"""
Hands-On Exercise: Implement a Real-Time Notification Consumer
Create a WebSocket consumer that listens for server-side events pushing notifications to a logged-in user.

Step 1: Implement a consumer NotificationConsumer in your app’s consumers.py that:

Accepts only authenticated users.
Joins a group named after the user’s username (e.g., notifications_<username> ).
Handles a custom event type notify that sends JSON data to the client containing notification details.
"""


class NotificationConsumerJson(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
            raise DenyConnection("Authentication required")
        self.group_name = f'notifications_{user.username}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notify(self, event):
        notification = event['notification']
        await self.send_json(notification)

"""
Building a Real-Time Notification System:

Step 5: Testing:

Run your Django development server with Channels support.
Open a browser and connect to the WebSocket endpoint ws://localhost:8000/ws/notifications/ using a WebSocket client or frontend JavaScript.
Trigger notifications by visiting:
http://localhost:8000/notifications/send/?message=Hello+World

Observe real-time notifications appear on the WebSocket client connected.

"""

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = "notifications_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def receive(self, text_data=None, bytes_data=None):
        pass# No client message handling for this example

    async def send_notification_notify(self, event):

        message = event["message"]
        await self.send(text_data=message)

def send_notification(request):
    message = request.GET.get('message', 'Hello, this is a notification!')
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications_group",
        {
            "type": "send_notification_notify",
            "message": message
        }
    )
    return JsonResponse({"status": "Notification sent!"})



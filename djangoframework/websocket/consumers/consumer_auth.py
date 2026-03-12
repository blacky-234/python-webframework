from channels.exceptions import DenyConnection
from channels.auth import AuthMiddlewareStack
from channels.generic.websocket import AsyncWebsocketConsumer
"""
Integrating Authentication and User State
Real-world applications often require authenticated WebSocket connections with user context. 
With AuthMiddlewareStack, you have access to the user object via self.scope['user'] in the consumer.
"""

class AuthenticationChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        if self.scope['user'].is_anonymouse:
            # Reject connection if user is anonymous
            await self.close()
            raise DenyConnection("Anonymous users are not allowed")
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.groups_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.groups_name, self.channel_name)
        await self.accept()
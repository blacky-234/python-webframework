from channels.generic.websocket import AsyncWebsocketConsumer
import json

"""
1)Allows connections to rooms by name.
2)Joins a channel group on connect.
3)Broadcasts any received message to all group members.
4)Sends messages asynchronously over the WebSocket.
"""
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'chat_{self.room_name}'

        #join the group corresponding to the room
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    

    async def disconnect(self, close_code):
        #leave the group when the connection is closed
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    
    #Receive message from WebSocket
    async def receive(self, text_data = None, bytes_data = None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Broadcast message to the group
        await self.channel_layer.group_send(self.group_name,{'type': 'chat_message', 'message': message})
    
    # Receive message from the group
    async def chat_message(self, event):

        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))
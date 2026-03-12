from channels.generic.websocket import AsyncWebsocketConsumer,JsonWebsocketConsumer,AsyncJsonWebsocketConsumer
import json

"""
Basic Consumer Skeleton
"""

class ChatConsumerSkeleton(AsyncWebsocketConsumer):

    async def connect(self):
        # Called when the websocket is handshaking as part of initial connection.
        await self.accept()  # Accept the connection
    
    async def disconnect(self, close_code):
        # Called when the socket closes
        pass

    async def receive(self, text_data=None, bytes_data=None):
        # Called when a message is received from the websocket
        if text_data:
            data = json.loads(text_data)
            message = data.get('message')

            # Echo the received message back to the client
            await self.send(text_data=json.dumps({
                'message': message
            }))

"""
Efficient Serialization: Handling JSON and Binary Data.
AsyncJsonWebsocketConsumer handles JSON encoding/decoding internally, minimizing boilerplate.

If your application requires binary data (e.g., images, files), use the bytes_data argument in receive() 
and handle accordingly. For example, you might base64 encode large data before sending it over WebSockets.
"""

class JsonChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def receive_json(self, content):
        message = content.get('message')
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat.message',
            'message': message,
        })
    
    async def chat_message(self, event):
        await self.send_json({
            'message': event['message']
        })


"""
1)Allows connections to rooms by name.
2)Joins a channel group on connect.
3)Broadcasts any received message to all group members.
4)Sends messages asynchronously over the WebSocket.

Handling WebSocket Exceptions and Reconnection Logic
Advanced consumers must deal with network faults and client disconnects effectively. 
Signals like disconnect give you hooks for cleanup, resource deallocation, or logging.

To handle errors gracefully inside consumers, use try-except blocks around async operations:
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

        if not text_data:
            return

        if not bytes_data:
            return
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            # Broadcast message to the group
            await self.channel_layer.group_send(self.group_name,{'type': 'chat_message', 'message': message})
        except json.JSONDecodeError:
            await self.send(text=json.dumps({'error': 'Invalid JSON data'}))
        except ValueError:
            message = text_data
        except Exception as e:
            # Log detailed error here
            await self.close(code=1011) # internal error close code
        


    
    # Receive meesgae
    async def chat_message(self, event):
        # Receive message from group
        message = event['message']

        # Send message to WebSocket client
        await self.send(text_data=message)
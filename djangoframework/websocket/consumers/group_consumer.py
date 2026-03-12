from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
"""
This approach illustrates bi-directional broadcasting with channel layers: 
clients send into the group and all subscribed clients receive the broadcasted message.

Benefits of Group Messaging
Centralized management of subscriptions.
Efficient broadcasting without direct knowledge of each client.
Supports scaling horizontally (multiple instances of your app).
"""

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_namme = 'chat_room'
        self.room_group_name= 'chat_group'

        #join room group
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
    
    #Receive message from WebSocket
    async def receive(self, text_data = None, bytes_data = None):

        if not text_data or text_data is None:
            return

        if not bytes_data or bytes_data is None:
            return
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            # Broadcast message to the group
            await self.channel_layer.group_send(self.room_group_name,{'type': 'chat_message', 'message': message})
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

"""
Handling Real-Time Data Streams and Backpressure:
When real-time data is high volume or bursty, you must manage the flow to avoid bottlenecks or crashes.

Backpressure Strategies:
Rate limiting: Use middleware or logic in consumers to limit message frequency per client.
Buffering and batching: Aggregate updates and send less frequently.
Flow control at client: Clients can signal readiness or pause consumption.
Timeouts and heartbeat messages: Detect inactive clients or dropped connections and cleanup.
Example of implementing a heartbeat in a Channels consumer to detect client disconnection:
"""

class HeartbeatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        self.ping_task =asyncio.create_task(self.send_pings())
    
    async def disconnect(self, close_code):
        self.ping_task.cancel()
    
    async def send_pings(self):
        try:
            while True:
                await self.send(text_data=json.dumps({'type': 'ping'}))
                await asyncio.sleep(10) # send ping every 10 seconds
        except asyncio.CancelledError:
            pass
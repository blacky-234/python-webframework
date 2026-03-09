from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio

class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("data connected in progress consumers")
        self.job_id = self.scope["url_route"]["kwargs"]["job_id"]
        self.group_name = f"job_{self.job_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def progress_update(self, event):
        await self.send(text_data=json.dumps(event))

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("data connected in notification consumers")
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def receive(self, text_data = None, bytes_data = None):
        # start a background task without awaiting it
        try:
            asyncio.create_task(self.background_task())
        except Exception as e:
            print(f"Error starting background task: {e}")

    
    async def background_notification_task(self):

        await asyncio.sleep(5)  # Simulate processing delay
        await self.channel_layer.group_send("notifications", {
            "type": "send_notification",
            "message": "This is a notification from the background task!"
        })


    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=message)

# Handling Long-lived Background Tasks with Django Async Workers

from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer

class Command(BaseCommand):

    help = "Async Background worker"

    def handle(self, *args, **options):
        asyncio.run(self.worker())
    
    async def worker(self):

        channel_layer = get_channel_layer()
        while True:

            #simulate work poling or waiting for event
            print("Worker is running...")
            await asyncio.sleep(10)

# Practical: Building a Live Background Task Notification Example

async def heavy_computation():
    # Simulate heavy background work
    await asyncio.sleep(10)
    return "Computation Result"

class Taskconsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def receive(self, text_data = None, bytes_data = None):
        result = await heavy_computation()
        await self.send(text_data=result)

class BackgroundTaskConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def receive(self, text_data = None, bytes_data = None):
        asyncio.create_task(self.do_background_task())
    
    async def do_background_task(self):
        await asyncio.sleep(10)
        await self.send(text_data="Background Task Completed!")

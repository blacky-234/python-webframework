"""
Building a Real-Time Stock Ticker with WebSockets
In this exercise, you will create a Django Channels consumer that streams live stock price updates to connected clients. 
Unlike the simple echo or chat examples, the data source will be simulated with periodic random stock price updates broadcasted to all clients subscribed to a stock ticker group.

"""

import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import random

class StockTickerConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.group_name = "stock_ticker"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # start send stock update in background
        self.send_task =asyncio.create_task(self.send_stock_updates())

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        self.send_task.cancel()
    
    async def send_stock_updates(self):

        try:
            while True:
                #simulate stock price update
                price = round(random.uniform(100, 500), 2)
                stock_data = {
                    'symbol': 'AAPL',
                    'price': price,
                    'timestamp': asyncio.get_event_loop().time()
                }

                #Broadcast update or group
                await self.channel_layer.group_send(self.group_name, {
                    'type': 'stock_update',
                    'data': stock_data
                })
        except asyncio.CancelledError:
            pass
    
    async def stock_update(self, event):

        stock_data = event['data']
        await self.send(text_data=json.dumps(stock_data))
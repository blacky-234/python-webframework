from .base import BaseWebSocket

class EchoConsumer(BaseWebSocket):
    async def receive_message(self, message: str):
        await self.send({
            "type": "websocket.send",
            "text": f"Echo: {message}"
        })

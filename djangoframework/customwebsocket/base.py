class BaseWebSocket:
    """
    Base reusable WebSocket handler.
    Subclass this to create your own consumers.
    """

    def __init__(self, scope, receive, send):
        self.scope = scope
        self.receive = receive
        self.send = send

    async def connect(self):
        """Called when a new WebSocket connection is accepted"""
        await self.send({"type": "websocket.accept"})

    async def disconnect(self, code):
        """Called when the WebSocket disconnects"""
        pass

    async def receive_message(self, message):
        """Handle incoming messages"""
        pass

    async def __call__(self):
        await self.connect()
        try:
            while True:
                event = await self.receive()

                if event["type"] == "websocket.disconnect":
                    await self.disconnect(event.get("code", 1000))
                    break

                if event["type"] == "websocket.receive":
                    if "text" in event:
                        await self.receive_message(event["text"])
        except Exception as e:
            print(f"WebSocket error: {e}")

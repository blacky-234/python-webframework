
from fastapi import WebSocket, WebSocketDisconnect,APIRouter
import asyncio

web_rt = APIRouter(
    prefix="/streams",
    tags=["streams"],
    responses={404: {"description": "Not found"}},
    )

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections.copy():
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)


manager = ConnectionManager()

@web_rt.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)



@web_rt.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        for i in range(10):
            await websocket.send_text(f"Update {i}")
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Stream client disconnected")



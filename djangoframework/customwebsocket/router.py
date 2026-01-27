from .consumers import EchoConsumer

routes = {
    "/ws/echo": EchoConsumer,
    # "/ws/kafka": KafkaConsumer,  (future)
}

async def websocket_router(scope, receive, send):
    path = scope.get("path")
    consumer_class = routes.get(path)

    if consumer_class is None:
        # Reject unknown paths
        await send({"type": "websocket.close", "code": 4000})
        return

    consumer = consumer_class(scope, receive, send)
    await consumer()

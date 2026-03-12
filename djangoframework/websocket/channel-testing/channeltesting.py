from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from websocket.consumers.consumers import basic_consumers
# from yourproject.asgi import application

class ChatConsumerTests(TransactionTestCase):
    async def test_chat_connect_and_receive(self):
        communicator = WebsocketCommunicator(basic_consumers.ChatConsumer, "/ws/chat/testroom/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({'message': 'Hello'})
        response = await communicator.receive_json_from()
        self.assertEqual(response, {'message': 'Hello'})

        await communicator.disconnect()
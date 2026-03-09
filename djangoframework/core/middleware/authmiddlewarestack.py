from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from usermanagement.models import User

"""
Optimizing Performance and Scalability
For production-ready apps, especially those serving many concurrent WebSocket connections, consider:

1)Using multiple Daphne or Uvicorn instances behind a load balancer.
2)Setting up Redis clusters for fault tolerance and high throughput.
3)Caching strategies for events in Redis to mitigate database load.
4)Monitoring channel layer latency and message queue lengths.
5)Applying backpressure and rate limiting on WebSocket connections.
6)Channels themselves are designed to scale horizontally via the channel layer's message broker, which acts as a pub-sub system
"""

@database_sync_to_async
def get_user(token):
    try:
        access_token = AccessToken(token)
        user = User.objects.get(id=token['user_id'])
        return user
    except Exception as e:
        print(f"Error decoding token: {e}")
        return AnonymousUser()

# TODO: This example is sophisticated but gives insight into middleware extensibility.
class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        query_string = scope['query_string'].decode()
        token_key = None
        # Extract token from query params or headers here
        # Example for query string ?token=xxx
        for param in query_string.split('&'):
            if param.startswith('token='):
                token_key = param.split('=')[1]

        scope['user'] = await get_user(token_key) if token_key else AnonymousUser()
        return await super().__call__(scope, receive, send)
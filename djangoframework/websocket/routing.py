from django.urls import re_path
from .consumers import BackgroundTaskConsumer


websocket_urlpatterns = [
    re_path(r'ws/background-task/$', BackgroundTaskConsumer.as_asgi()),
]
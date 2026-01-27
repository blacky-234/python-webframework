# Live Report Generator — WebSocket realtime push UI

This document contains all the code snippets and run instructions to add **WebSocket realtime push** to the Django + Celery (RabbitMQ) project described earlier.

---

## Summary

Architecture used here:
- Django (normal project)
- Celery + RabbitMQ for long-running background job
- Django Channels + Redis channel layer for WebSocket push (workers push progress to channels)
- Frontend connects to a WebSocket and receives progress updates in real-time

You will need to run Redis (for channels) and RabbitMQ (for Celery) at the same time.

---

### 0. Install packages

```bash
pip install channels channels_redis daphne
# celery is already installed per previous steps
# rabbitmq-server and redis-server should be installed and running on the host
# e.g. on Debian/Ubuntu:
# sudo apt update
# sudo apt install redis-server rabbitmq-server -y
# sudo systemctl enable --now redis-server rabbitmq-server
```

---

### 1) Project settings changes (live_report_project/settings.py)

Add channels to INSTALLED_APPS and configure ASGI and channel layer:

```python
# settings.py (additions / edits)
INSTALLED_APPS = [
    # ... existing apps ...
    'channels',
    'reports',
]

# Channels
ASGI_APPLICATION = 'live_report_project.asgi.application'

# Channel layer (Redis)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

# Celery config (keep RabbitMQ broker you had before)
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'rpc://'
```

---

### 2) ASGI entrypoint (live_report_project/asgi.py)

```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import reports.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'live_report_project.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': URLRouter(reports.routing.websocket_urlpatterns),
})
```

---

### 3) WebSocket routing (reports/routing.py)

```python
# reports/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/reports/(?P<job_id>[0-9a-fA-F-]+)/$', consumers.ReportProgressConsumer.as_asgi()),
]
```

---

### 4) Consumer (reports/consumers.py)

```python
# reports/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ReportProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        self.group_name = f'report_{self.job_id}'

        # join group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # leave group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # handler that celery will call via group_send
    async def progress_update(self, event):
        # event is a dict; send to WebSocket as JSON
        await self.send(text_data=json.dumps({
            'progress': event.get('progress'),
            'status': event.get('status'),
            'message': event.get('message', ''),
        }))

    # optional: receive from client
    async def receive(self, text_data=None, bytes_data=None):
        # You can implement client->server messages if needed
        pass
```

Note: the handler name `progress_update` corresponds to the `type` key used in `group_send` (see Celery task below).

---

### 5) Celery task: send progress updates through channel layer (reports/tasks.py)

```python
# reports/tasks.py
import time
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ReportJob

@shared_task(bind=True)
def generate_report(self, job_id):
    channel_layer = get_channel_layer()
    group_name = f'report_{job_id}'

    # simulate work: 10 steps; replace with real work
    for i in range(1, 11):
        time.sleep(60)  # 1 minute per step in earlier example
        percent = i * 10

        # update DB progress
        ReportJob.objects.filter(job_id=job_id).update(progress=percent, status='in_progress')

        # send real-time progress to connected websocket clients
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'progress_update',  # maps to ReportProgressConsumer.progress_update
                'progress': percent,
                'status': 'in_progress',
                'message': f'{percent}% complete',
            }
        )

    # finish
    ReportJob.objects.filter(job_id=job_id).update(progress=100, status='completed')
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'progress_update',
            'progress': 100,
            'status': 'completed',
            'message': 'Report completed',
        }
    )

    return {'status': 'ok'}
```

Notes:
- We use `async_to_sync` because Celery task runs in a synchronous worker process.
- `channel_layer` resolves to Redis channel layer (must be running).

---

### 6) Start endpoint (views) — returns job_id and starts celery task

```python
# reports/views.py
from django.http import JsonResponse
from .tasks import generate_report
from .models import ReportJob
import uuid


def start_report_job(request):
    job_id = str(uuid.uuid4())
    ReportJob.objects.create(job_id=job_id, status='started', progress=0)
    # kick off celery task (non-blocking)
    generate_report.delay(job_id)
    return JsonResponse({'job_id': job_id, 'message': 'Report started'})
```

---

### 7) Frontend: WebSocket client and progress UI (templates/reports/report_dashboard.html)

```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Report Dashboard</title>
  <style>
    .progress { width: 100%; background: #eee; border-radius: 6px; height: 24px; overflow: hidden }
    .bar { height: 100%; width: 0%; background: linear-gradient(90deg, #4caf50, #8bc34a); transition: width .25s }
  </style>
</head>
<body>
  <button id="start-btn">Start Report</button>
  <div id="job-area" style="display:none; margin-top: 20px;">
    <div>Job ID: <span id="job-id"></span></div>
    <div class="progress" style="margin-top:8px;"><div id="bar" class="bar"></div></div>
    <div id="status" style="margin-top:8px"></div>
  </div>

  <script>
    const startBtn = document.getElementById('start-btn');
    const jobArea = document.getElementById('job-area');
    const jobIdEl = document.getElementById('job-id');
    const bar = document.getElementById('bar');
    const statusEl = document.getElementById('status');

    function getWsProtocol() {
      return (location.protocol === 'https:') ? 'wss://' : 'ws://';
    }

    startBtn.onclick = async () => {
      const resp = await fetch('/reports/start/');
      const data = await resp.json();
      const job_id = data.job_id;

      jobIdEl.textContent = job_id;
      jobArea.style.display = 'block';

      // open websocket
      const wsUrl = getWsProtocol() + location.host + `/ws/reports/${job_id}/`;
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        statusEl.textContent = 'Connected — waiting for progress...';
      };

      ws.onmessage = (message) => {
        try {
          const payload = JSON.parse(message.data);
          const p = payload.progress || 0;
          bar.style.width = p + '%';
          statusEl.textContent = payload.status + (payload.message ? ' — ' + payload.message : '');
          if (payload.status === 'completed') {
            statusEl.textContent = 'Completed';
            ws.close();
          }
        } catch (e) {
          console.error('invalid message', e);
        }
      };

      ws.onclose = () => {
        statusEl.textContent = (statusEl.textContent === 'Completed') ? 'Completed' : 'Disconnected';
      };

      ws.onerror = (err) => {
        console.error('WebSocket error', err);
        statusEl.textContent = 'Error';
      };
    };
  </script>
</body>
</html>
```

Notes:
- The frontend connects to `/ws/reports/<job_id>/` and listens to JSON messages.
- Uses `location.host` to work across environments.

---

### 8) Run commands (terminals)

1) Start Redis
```bash
sudo systemctl start redis-server
```

2) Start RabbitMQ (already mentioned earlier)
```bash
sudo systemctl start rabbitmq-server
```

3) Run migrations and Django server (you can run Daphne to enable ASGI/http + websockets):
```bash
python manage.py migrate
# start daphne (serves HTTP and WebSocket via ASGI)
daphne -b 0.0.0.0 -p 8000 live_report_project.asgi:application
```

4) Start Celery worker (in separate terminal):
```bash
celery -A live_report_project worker --loglevel=info
```

Alternative: during local development you can run `python manage.py runserver` for HTTP and run a separate Daphne for websockets, but the recommended is to use Daphne as ASGI server.

---

### 9) Security & production notes

- For production, use secure WebSocket (wss://) behind TLS termination (nginx or load balancer).
- Channel layer Redis must be secured and not openly accessible.
- Use authentication for WebSocket connections (e.g. cookie-based session authentication or token-based). The above consumer is unauthenticated for clarity; add `channels.auth` middleware if required.
- If using Docker compose, you can run rabbitmq, redis, django, celery worker, and daphne as services.

---

### 10) Optional: Authenticate WebSocket connections

To send authenticated updates only to authorized users, use `channels.auth.AuthMiddlewareStack` in your `asgi.py` (wrap URLRouter) and inspect `self.scope['user']` inside the consumer.

Example ASGI update:

```python
from channels.auth import AuthMiddlewareStack
application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(reports.routing.websocket_urlpatterns)
    ),
})
```

---

That's everything for a working realtime push pipeline. If you want, I can also:
- Produce a ready-to-run `docker-compose.yml` that brings up Redis, RabbitMQ, Django, Celery, and Daphne, or
- Generate a single zipped example repository with these files, or
- Add authentication and token-based websocket auth to the example.

Open this document in the canvas to copy files and run them locally.

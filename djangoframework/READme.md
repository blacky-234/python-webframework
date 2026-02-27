# Project Overview

This project focuses on **backend development** using Django and related technologies to build a scalable and real-time system.

## Key Features

- 🔄 **Real-time updates** using **WebSockets** with **Django Channels**
- ⚙️ **Asynchronous background processing** using **Celery** with **RabbitMQ**
- 🔐 **Atomic database operations** to ensure data consistency during product and order updates
- 🚀 Optimized database queries for performance

## Technologies Used

- Django
- Django Channels (WebSocket support)
- Celery
- RabbitMQ
- PostgreSQL / MySQL
- Redis (optional, for Channels & Celery)
- Linux-based deployment

## Database Optimization Techniques

- `select_related()` for ForeignKey & OneToOne relationships
- `prefetch_related()` for ManyToMany relationships
- `select_for_update()` for row-level locking during atomic transactions
- `transaction.atomic()` for safe concurrent updates

## Use Cases

- Real-time order status updates
- Background processing of long-running tasks
- High-concurrency product/order management
- Efficient handling of relational data

## Status

🚧 Backend-focused project (Frontend integration optional)


## Celery Configurations

pip install celery
pip install channel
pip install redis
pip install django-redis
pip install channels 
pip install channels-redis 
pip install uvicorn



## docker 

1. database :

6ac611a9927e  - djangoframework   - database - 172.21.0.3

2. memcache

f5b624f1e459   memcatchdjangoframework - 172.21.0.4

3. rabbitmq

c5d3b49e00b9  myrabbitmq - 172.21.0.5

4. redis

9bcc415ea93f  RedisLearning - 172.21.0.6


## start celery worker and beat commands

```celery -A mainsrc worker --beat --loglevel=info```


## start websocket using uvicorn

```uvicorn mainsrc.asgi:application --reload```


## Connect to React

```bash
pip install django-cors-headers
```

```python

INSTALLED_APPS = [
    ...
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

```

## Advanced Django Models & Query Optimization


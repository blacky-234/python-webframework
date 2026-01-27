import time
from celery import shared_task
from .models import ReportJob
from django.core.cache import caches
import uuid
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# @shared_task(bind=True)
# def generate_report(self, job_id):
#     redis_cache = caches['redis']   # use redis cache backend
#     redis_key = f"report_progress:{job_id}"

#     for i in range(1, 11):
#         time.sleep(60)  # simulate heavy work for 10 minutes
#         percent = i * 10

#         # 1️⃣ Save progress to Redis (FAST / ATOMIC)
#         redis_cache.set(redis_key, percent, timeout=7200)

#         # 2️⃣ (Optional) Using Celery internal progress state
#         self.update_state(
#             state="PROGRESS",
#             meta={"progress": percent}
#         )

#         print(f"report percentage get in redis: {redis_cache.get(redis_key)}")

#     # 3️⃣ When complete → update DB ONCE
#     ReportJob.objects.filter(job_id=job_id).update(
#         status="completed",
#         progress=100
#     )

#     # 4️⃣ Remove temporary key
#     redis_cache.delete(redis_key)

#     print("✅ Report Completed using Redis-based progress")
#     return "Report ready"


@shared_task
def generate_report(job_id):
    channel_layer = get_channel_layer()

    for i in range(1, 101):
        time.sleep(0.1)

        async_to_sync(channel_layer.group_send)(
            f"job_{job_id}",
            {
                "type": "progress_update",
                "progress": i
            }
        )
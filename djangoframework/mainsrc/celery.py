from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
# from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainsrc.settings")

app = Celery("mainsrc")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

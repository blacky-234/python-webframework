from django.urls import path
from .views import SystemStatus,ReportStatus
from websocket.consumers.consumers import ProgressConsumer
from websocket.consumers.consumer_json import send_notification

app_name = 'websocket'

SystemPath = [
    path('',SystemStatus.system_status, name='systemstatus'),
]

Report = [
    path('start/', ReportStatus.start_report_job),
    path('progress/<str:job_id>/', ReportStatus.check_report_progress),
]


testingwebsocket = [
    path('progr/<str:job_id>/', ProgressConsumer.as_asgi()),
]

websocket_http = [
    path('send/', send_notification, name='send_notification'),
]


urlpatterns = SystemPath+Report+websocket_http
from django.shortcuts import render
from django.http import JsonResponse
from .tasks import generate_report
from .models import ReportJob
import uuid
import asyncio
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.template.loader import render_to_string

# Create your views here.

class SystemStatus:
    def system_status(request):
        if request.method == 'GET':
            context = {}
            context['report'] = ReportJob.objects.all()
            return render(request, 'systemstatus.html',context)

class ReportStatus:

    # Normal endpoint starts celery task
    @api_view(['GET'])
    def start_report_job(request):
        print("Starting report job")
        context = {}
        job_id = str(uuid.uuid4())
        report = ReportJob.objects.create(job_id=job_id, status="started")
        context['job'] = ReportJob.objects.get(id=report.id)
        generate_report.delay(job_id)
        data = render_to_string('tablerow.html', context)
        job_id = report.job_id
        return Response({"job_id": job_id, "html": data},status.HTTP_200_OK)

    # Async endpoint for checking progress (non-blocking)
    async def check_report_progress(request, job_id):
        await asyncio.sleep(0)  # allows event loop to switch task
        job = ReportJob.objects.get(job_id=job_id)
        return JsonResponse({"job_id": job_id, "progress": job.progress, "status": job.status})

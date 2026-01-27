from django.db import models

# Create your models here.
class ReportJob(models.Model):

    job_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, default='start')
    progress = models.IntegerField(default=0)
    result_file = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:

        db_table = 'report_jobs'

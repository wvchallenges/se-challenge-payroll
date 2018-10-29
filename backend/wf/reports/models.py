from django.db import models


class TimeReportEntry(models.Model):
    JOB_GROUPS = (
        ('A', 'A'),
        ('B', 'B'),
    )
    date = models.DateField()
    hours_worked = models.FloatField()
    employee_id = models.IntegerField()
    job_group = models.CharField(choices=JOB_GROUPS, max_length=1)
    time_report = models.ForeignKey('TimeReport', on_delete=models.CASCADE)


class TimeReport(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
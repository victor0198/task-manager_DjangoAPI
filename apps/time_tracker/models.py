from django.db import models
from apps.task.models import Task


class TimeTracker(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

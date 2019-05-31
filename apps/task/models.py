from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Task(models.Model):
    user_created = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_creat")
    user_assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_assign", null=True,
                                      default=None)
    title = models.CharField(max_length=100)
    description = models.TextField()
    CREATED = 'created'
    INPROCESS = 'inprocess'
    FINISHED = 'finished'
    STATUS_CHOICES = [
        (CREATED, 'created'),
        (INPROCESS, 'inprocess'),
        (FINISHED, 'finished'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=CREATED)
    date_create_task = models.DateTimeField(null=True, blank=True)
    update_task = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField (default=0)
    @staticmethod
    def is_finished(self):
        return self.status == Task.FINISHED

    @staticmethod
    def get_status(self):
        return self.status



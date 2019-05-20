from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    user_created = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_creat")
    user_assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_assign", null=True, default=None)
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

    @property
    def is_created(self):
        return self.status == Task.CREATED

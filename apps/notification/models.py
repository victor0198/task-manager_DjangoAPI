from django.db import models
from apps.task.models import Task
from apps.comment.models import Comment
from django.contrib.auth.models import User


# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ManyToManyField(Task)
    comment = models.ManyToManyField(Comment)
    seen = models.BooleanField()

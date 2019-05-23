from django.db import models
from apps.task.models import Task
from apps.comment.models import Comment
from django.contrib.auth.models import User


# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    seen = models.BooleanField()
    status = models.CharField(max_length=10, null=True)

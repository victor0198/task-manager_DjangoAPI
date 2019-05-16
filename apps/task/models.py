from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    user_created = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_creat")
    user_assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_assign")
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ManyToManyField(Task)
    comment = models.ManyToManyField(Comment)
 
from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    user_created = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_creat")
    user_assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_assign")
    title = models.CharField(max_length=100)
    description = models.TextField()
    CREATED = '0'
    INPROCES = '1'
    FINISHED = '2'
    STATUS_CHOICES = [
        (CREATED, '0'),
        (INPROCES, '1'),
        (FINISHED, '2'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=CREATED)
    date_created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ManyToManyField(Task)
    comment = models.ManyToManyField(Comment)


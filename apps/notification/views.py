from django.shortcuts import render
from drf_util.decorators import serialize_decorator

from apps.task.serializers import TaskSerializer, TaskSelfSerializer
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from apps.task.models import Notification, Task, Comment
from rest_framework.response import Response
from apps.notification.serializers import NotificationSerializer
from django.contrib.auth.models import User


def AddNotificationComment(iduser, comment):
    userinstance = User.objects.filter(id=iduser).first()

    notification = Notification.objects.create(
        user=userinstance
    )
    notification.comment.add(comment)
    notification.save()


def AddNotificationTask(iduser, task):
    userinstance = User.objects.filter(id=iduser).first()

    notification = Notification.objects.create(
        user=userinstance
    )
    notification.task.add(task)
    notification.save()


# task 15: View my notifications

class MyNotificationSerializer(GenericAPIView):
    serializer_class = NotificationSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        notific = Notification.objects.filter(user=pk)
        return Response(NotificationSerializer(notific, many=True).data)

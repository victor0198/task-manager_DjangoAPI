from django.shortcuts import render
from drf_util.decorators import serialize_decorator

from apps.task.serializers import TaskSerializer, TaskSelfSerializer
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from apps.task.models import  Task
from apps.notification.models import Notification
from apps.comment.models import Comment
from rest_framework.response import Response
from apps.notification.serializers import NotificationSerializer
from django.contrib.auth.models import User


def AddNotificationComment(user, comment):
    notification = Notification.objects.create(
        user=user,
        seen=False
    )
    notification.comment.add(comment)
    notification.save()


def AddNotificationTask(user, task):
    notification = Notification.objects.create(
        user=user,
        seen=False
    )
    notification.task.add(task)
    notification.save()


def AddNotificationTaskClosed(user, task):
    notification = Notification.objects.create(
        user=user,
        seen=False
    )
    notification.task.add(task)
    notification.save()


# task 4: Create a task
class AddNotificationView(GenericAPIView):
    serializer_class = NotificationSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(NotificationSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        task = Task.objects.create(
            title=validated_data['title'],
        )
        task.save()

        return Response(NotificationSerializer(task).data)


# task 15: View my notifications

class MyNotificationView(GenericAPIView):
    serializer_class = NotificationSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        notific = Notification.objects.filter(user=pk)
        return Response(NotificationSerializer(notific, many=True).data)


# task 16: View count of new notifications

class CountNewNotifications(GenericAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        not_true = Notification.objects.filter(seen=False)
        count = len(not_true)
        return Response({"count=": count})
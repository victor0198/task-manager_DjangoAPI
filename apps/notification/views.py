from drf_util.decorators import serialize_decorator

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.notification.models import Notification
from apps.task.models import Task

from rest_framework.response import Response
from apps.notification.serializers import NotificationSerializer


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





# task 15: View my notifications

class MyNotificationView(GenericAPIView):
    serializer_class = NotificationSerializer

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        notific = Notification.objects.filter(user=request.user.id)
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


from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.notification.models import Notification
from rest_framework.response import Response
from apps.notification.serializers import NotificationSerializer


def AddNotificationComment(user, comment, task):
    notification = Notification.objects.create(
        user=user,
        task=task,
        comment=comment,
        seen=False,
        status=None
    )

    notification.save()


def AddNotificationTaskStatus(user, task, status):
    notification = Notification.objects.create(
        user=user,
        task=task,
        seen=False,
        status=status
    )

    notification.save()


# task 15: View my notifications

class MyNotificationView(GenericAPIView):

    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        notific = Notification.objects.filter(user=request.user.id, seen=False).order_by("-id")
        return Response(NotificationSerializer(notific, many=True).data)


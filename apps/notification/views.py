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
        url_parameters = str(request.META['QUERY_STRING'])
        params = url_parameters.split('&')
        notifications = None

        for param in params:
            if param:
                key = param.split('=')[0]
                if int(param.split('=')[1]) >= 0:
                    valueStart = (int(param.split('=')[1])) * 10
                    valueEnd = int(valueStart) + 10
                    if key == 'page':
                        notifications = Notification.objects.filter(user=request.user.id, seen=False).order_by("-id")[
                                        int(valueStart):int(valueEnd)]

                        # there are no notifications on this page
                        if not notifications:
                            return Response(status=204)
                else:
                    return Response(status=400)

        if not notifications:
            notifications = Notification.objects.filter(user=request.user.id, seen=False).order_by("-id")[:10]

        response = dict({"notifications": NotificationSerializer(notifications, many=True, context={'user_id': request.user.id}).data.copy()})
        total_notifications = Notification.objects.filter(user=request.user.id, seen=False).count()
        response.update({"count": total_notifications})



        return Response(response)

from drf_util.decorators import serialize_decorator

from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from apps.task.models import Notification, Task
from rest_framework.response import Response
from apps.notification.serializers import NotificationSerializer



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


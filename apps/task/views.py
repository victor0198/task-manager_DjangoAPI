from django.contrib.auth.models import User
from drf_util.decorators import serialize_decorator
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.task.models import Task, Comment
from apps.task.serializers import DetailTaskSerializer, TaskSerializer, TaskUpdateStatus


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer


# task 11
class TaskCommentsView(GenericAPIView):
    serializer_class = DetailTaskSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        response_data = DetailTaskSerializer(task).data
        return Response(response_data)


# task 5
class UserTaskView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        task = Task.objects.filter(user_assigned=pk)
        return Response(TaskSerializer(task, ).data)


# task 8
class FinishTask(GenericAPIView):
    serializer_class = TaskUpdateStatus
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(TaskUpdateStatus)
    def put(self, request):
        serializer = TaskUpdateStatus(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            task = Task.objects.filter(id=data["id"]).first()
            task.status = 2
            task.save()
            return Response(TaskSerializer(task).data)

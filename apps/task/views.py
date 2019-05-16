from drf_util.decorators import serialize_decorator
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.task.models import Task, Comment, Notification
from apps.task.serializers import TaskSerializer

"""
    TASK SWAGGER view
"""


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


# View list of tasks

class TaskListView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        task = Task.objects.all()

        return Response(TaskSerializer(task, many=True).data)


# View Completed tasks

class CompletedTaskListView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        task = Task.objects.filter(pk=Task.FINISHED)

        return Response(TaskSerializer(task, many=True).data)


# Remove task

class DeleteView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        task.delete()
        return Response(TaskSerializer(task).data)

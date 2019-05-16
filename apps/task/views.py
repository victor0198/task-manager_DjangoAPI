from django.shortcuts import render
from drf_util.decorators import serialize_decorator
from rest_framework import viewsets

from apps.task.serializers import TaskSerializer, TaskSelfSerializer
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from apps.task.models import Task
from rest_framework.response import Response


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

    @serialize_decorator(TaskSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        task = Task.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            status=validated_data['status'],
            user_created=validated_data['user_created'],
            user_assigned=validated_data['user_assigned'],
        )
        task.save()

        return Response(TaskSerializer(task).data)


# task 7: Assign a task to me
class AddTaskSelfView(GenericAPIView):
    serializer_class = TaskSelfSerializer
    def get(self, request):
        task = Task.objects.all()

        return Response(TaskSerializer(task, many=True).data)


# task3: View Completed tasks

class CompletedTaskListView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(TaskSelfSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        task = Task.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            status=validated_data['status'],
            user_created=validated_data['user_created'],
            user_assigned=validated_data['user_created'],
        )
        task.save()

        return Response(TaskSelfSerializer(task).data)
    def get(self, request):
        task = Task.objects.filter(pk=Task.FINISHED)

        return Response(TaskSerializer(task, many=True).data)


# task 9: Remove task

class DeleteView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        task.delete()
        return Response(TaskSerializer(task).data)

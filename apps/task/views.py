from django.shortcuts import render
from drf_util.decorators import serialize_decorator

from apps.task.serializers import TaskSerializer, TaskSelfSerializer
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from apps.task.models import Task
from rest_framework.response import Response


# task 4: Create a task
class AddTaskView(GenericAPIView):
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

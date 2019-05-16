from drf_util.decorators import serialize_decorator
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.task.models import Task, Comment, Notification
from apps.task.serializers import TaskSerializer, TaskSelfSerializer
from apps.notification.views import AddNotificationTask

"""
    TASK SWAGGER view qwe
"""


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


# Task 3: View list of tasks
class TaskListView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        task = Task.objects.all()
        return Response(TaskSerializer(task, many=True).data)


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


# Task 6: View Completed tasks
class CompletedTaskListView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        task = Task.objects.filter(status=Task.FINISHED)

        return Response(TaskSerializer(task, many=True).data)


# Task 9:  Remove task
class DeleteView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        task.delete()
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

        AddNotificationTask(task.user_assigned.id, task)

        return Response(TaskSelfSerializer(task).data)

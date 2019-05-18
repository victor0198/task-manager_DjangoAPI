from drf_util.decorators import serialize_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from apps.task.serializers import FilterTaskSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT
from apps.task.serializers import TaskSelfSerializer
from apps.task.models import Task
from apps.task.serializers import DetailTaskSerializer, TaskSerializer, TaskSerializerCreate, MyFilterSerializer,\
                                    TaskCommentsSerializer
from apps.notification.views import AddNotificationTask


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
    serializer_class = TaskSerializerCreate

    permission_classes = (IsAuthenticated,)

    @serialize_decorator(TaskSerializerCreate)
    def post(self, request):
        validated_data = request.serializer.validated_data

        task = Task.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            status=validated_data['status'],
            user_created=request.user,
            user_assigned=validated_data['user_assigned'],
        )
        task.save()

        AddNotificationTask(task.user_assigned, task)

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

    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        task.delete()
        return Response(status=HTTP_204_NO_CONTENT)


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

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        task = Task.objects.filter(user_assigned=request.user.id)
        return Response(TaskSerializer(task, many=True).data)


# task 7: Assign a task to me
class AddTaskSelfView(GenericAPIView):
    serializer_class = TaskSelfSerializer

    permission_classes = (IsAuthenticated,)

    @serialize_decorator(TaskSelfSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        task = Task.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            status=validated_data['status'],
            user_created=request.user,
            user_assigned=request.user,
        )
        task.save()

        AddNotificationTask(task.user_assigned.id, task)

        return Response(TaskSerializer(task).data)


# task 8
class FinishTask(GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def put(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.status = "finished"
        task.save()
        return Response(TaskSerializer(task).data)


# task 11 filter

class FilterTask(GenericAPIView):
    serializer_class = FilterTaskSerializer

    serializer_class = MyFilterSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(FilterTaskSerializer)
    @swagger_auto_schema(query_serializer=FilterTaskSerializer)
    def get(self, request):
        validated_data = request.serializer.validated_data
        task = Task.objects.filter(status=validated_data["status"], title=validated_data["title"],
                                   user_assigned=validated_data["user_assigned"])
        return Response(TaskSerializer(task, many=True).data)


class TaskItemCommentsView(GenericAPIView):
    serializer_class = TaskCommentsSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        blog = get_object_or_404(Task.objects.filter(pk=pk))
        response_data = TaskCommentsSerializer(blog).data
        return Response(response_data)
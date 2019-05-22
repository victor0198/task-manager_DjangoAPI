from datetime import datetime
from django.http import JsonResponse
from drf_util.decorators import serialize_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from apps.task.serializers import TaskUpdateAllSerializer, TaskSearchSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT
from apps.task.serializers import TaskSelfSerializer
from apps.task.models import Task
from apps.task.serializers import DetailTaskSerializer, TaskSerializer, TaskSerializerCreate, MyFilterSerializer, \
    TaskCommentsSerializer, TaskUpdateStateSerializer
from apps.notification.views import AddNotificationTask
from apps.users.serializers import UserTaskSerializer
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from apps.notification.models import Notification
from apps.comment.models import Comment


class TenResultsSetPagination(PageNumberPagination):
    page_size = 10


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    serializer_class = TaskSerializer
    queryset = Task.objects.order_by('-id')

    pagination_class = TenResultsSetPagination
    http_method_names = ['get']


class TaskFilterStatusCreatedViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    serializer_class = TaskSerializer
    queryset = Task.objects.filter(status=Task.CREATED).order_by('-id')

    pagination_class = TenResultsSetPagination
    http_method_names = ['get']


class TaskFilterStatusInprocessViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    serializer_class = TaskSerializer
    queryset = Task.objects.filter(status=Task.INPROCESS).order_by('-id')

    pagination_class = TenResultsSetPagination
    http_method_names = ['get']


class TaskFilterStatusFinishedViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    serializer_class = TaskSerializer
    queryset = Task.objects.filter(status=Task.FINISHED).order_by('-id')

    pagination_class = TenResultsSetPagination
    http_method_names = ['get']


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
            status=Task.CREATED,
            user_created=request.user,
            date_create_task=datetime.now()
        )
        if validated_data['user_assigned']:
            task.user_assigned = validated_data['user_assigned']

        task.save()

        if validated_data['user_assigned']:
            AddNotificationTask(task.user_assigned, task)

        return Response(status=201)


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
        task = Task.objects.filter(pk=pk, user_created=request.user.id)
        print(task)

        if task.count() == 0:
            return Response(status=403)
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

        for comment in response_data.items():
            if isinstance(comment[1], list):
                if len(comment[1]) > 1:
                    a_comment = dict(comment[1][0])
                    id_comment = a_comment.get('id')
                    comment_object = Comment.objects.get(id=id_comment)
                    id_task = comment_object.task

                    print(id_comment)
                    print(id_task.id)

                    if Notification.objects.filter(task=id_task.id):
                        notification = Notification.objects.get(task=task.id)
                        notification.seen = True
                        notification.save()

        if Notification.objects.filter(task=task.id):
            notification = Notification.objects.get(task=task.id)
            notification.seen = True
            notification.save()

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

        return Response(TaskSerializer(task).data)


# task 8
class UpdateTaskState(GenericAPIView):
    serializer_class = TaskUpdateStateSerializer

    permission_classes = (IsAuthenticated,)

    @serialize_decorator(TaskUpdateStateSerializer)
    def put(self, request):
        validated_data = request.serializer.validated_data
        task = Task.objects.get(pk=validated_data["id"])
        if (task.user_assigned and request.user.id == task.user_assigned.id) or request.user.id == task.user_created.id:
            task.status = validated_data["status"]
            task.save()
        else:
            return Response(status=403)

        return Response(TaskSerializer(task).data)


# task 11 filter
class FilterTask(GenericAPIView):
    serializer_class = MyFilterSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(MyFilterSerializer)
    @swagger_auto_schema(query_serializer=MyFilterSerializer)
    def get(self, request):
        validated_data = request.serializer.validated_data
        task = Task.objects.filter(status=validated_data["status"], title=validated_data["title"],
                                   user_assigned=validated_data["user_assigned"])
        return Response(TaskSerializer(task, many=True).data)


class TaskItemCommentsView(GenericAPIView):
    serializer_class = TaskCommentsSerializer

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        response_data = TaskCommentsSerializer(task).data
        return Response(response_data)


class TasksAllView(GenericAPIView):
    serializer_class = TaskSerializer, UserTaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        print("-1--")
        tasks_all = []
        tasks = Task.objects.all()

        for task in tasks:
            temp_task = TaskSerializer(task).data
            temp_task.update({'created by': UserTaskSerializer(User.objects.filter(pk=task.user_assigned.id).first())})
            tasks_all.append(temp_task)

        print("-2--")
        return JsonResponse(tasks_all, safe=False)


class UpdateTask(GenericAPIView):
    serializer_class = TaskUpdateAllSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def put(self, request):
        serializer = TaskUpdateAllSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            task = Task.objects.get(id=data['id'])
            task.user_created = data["user_created"]
            task.user_assigned = data["user_assigned"]
            task.title = data["title"]
            task.description = data["description"]
            task.status = data["status"]
            task.save()

            AddNotificationTask(task.user_assigned, task)

            response_data = TaskSerializer(task).data
            return Response(response_data)
        else:
            return Response(serializer.errors, status=400)


class TaskSearchViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    serializer_class = TaskSearchSerializer
    queryset = Task.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('$title', '$description')
    http_method_names = ['get']

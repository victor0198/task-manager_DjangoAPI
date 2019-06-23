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
from apps.task.serializers import DetailTaskSerializer, TaskSerializer, TaskSerializerCreate, TaskUpdateStateSerializer, \
    TasksAllSerializer
from apps.notification.views import AddNotificationTaskStatus
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from apps.notification.models import Notification
from apps.comment.models import Comment
import base64
import json
from apps.time_tracker.models import TimeTracker
from rejson import Client, Path


class TenResultsSetPagination(PageNumberPagination):
    page_size = 10


class AllRedisTasksView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        rj = Client(host='localhost', port=6379, )

        url_parameters = str(request.META['QUERY_STRING'])
        params = url_parameters.split('&')
        task = list()

        for param in params:
            if param:
                if param and int(param.split('=')[1]) >= 0 and param.split('=')[0] == "page":
                    valueStart = (int(param.split('=')[1])*10)
                    valueEnd = int(valueStart) + 10
                    tasksList = sorted(rj.execute_command('keys task:*'), reverse=True)

                    for item in tasksList[valueStart:valueEnd]:
                        current_task = getJSON(rj, item.decode('utf-8'), Path.rootPath())
                        if current_task:
                            task.append(current_task)

                    if not task:
                        return Response(status=204)
                else:
                    return Response(status=400)

        if not task:
            tasksList = sorted(rj.execute_command('keys task:*'), reverse=True)

            for item in tasksList[0:10]:
                current_task = getJSON(rj, item.decode('utf-8'), Path.rootPath())
                if current_task:
                    task.append(current_task)

        return Response(task)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    serializer_class = TasksAllSerializer
    queryset = Task.objects.order_by('-id')

    pagination_class = TenResultsSetPagination
    http_method_names = ['get']


class TaskFilterStatusCreatedViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    serializer_class = TasksAllSerializer
    queryset = Task.objects.filter(status=Task.CREATED).order_by('-id')

    pagination_class = TenResultsSetPagination
    http_method_names = ['get']


class TaskFilterStatusInprocessViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    serializer_class = TasksAllSerializer
    queryset = Task.objects.filter(status=Task.INPROCESS).order_by('-id')

    pagination_class = TenResultsSetPagination
    http_method_names = ['get']


class TaskFilterStatusFinishedViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    serializer_class = TasksAllSerializer
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

        if validated_data['user_assigned'] and validated_data['user_assigned'] != request.user:
            AddNotificationTaskStatus(task.user_assigned, task, "created")

        # add in ReJSON database
        rj = Client(host='localhost', port=6379, )
        rj.jsonset('task:' + str(task.id), Path.rootPath(), TaskSerializer(task).data)
        rj.execute_command('JSON.NUMINCRBY acc .total 1')
        rj.execute_command('JSON.SET acc .maxId ' + str(task.id))

        return Response(status=201)


def getJSON(rj, name, path):
    response_data = rj.execute_command('JSON.GET ' + name + ' ' + path)
    if not response_data:
        return None
    else:
        return json.loads(rj.execute_command('JSON.GET ' + name + ' ' + path).decode('utf-8'))


def deleteRedisJSON(rj):
    rj.execute_command('FLUSHDB')


class RedisInitView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        rj = Client(host='localhost', port=6379, )

        deleteRedisJSON(rj)

        tasks = Task.objects.all()
        for task in tasks:
            rj.jsonset('task:' + str(task.id), Path.rootPath(), TaskSerializer(task).data)

        accountant = dict()
        accountant.update({"total": tasks.count()})
        accountant.update({"maxId": tasks.last().id})
        rj.jsonset('acc', Path.rootPath(), accountant)

        return Response(status=200)


# Task 9:  Remove task
class DeleteView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        task = Task.objects.filter(pk=pk, user_created=request.user.id)

        if task.count() == 0:
            return Response(status=403)
        task.delete()
        return Response(status=HTTP_204_NO_CONTENT)


# task 11
class TaskCommentsView(GenericAPIView):
    serializer_class = DetailTaskSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk=0):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split()

            if not token[1] == "undefined":
                id_user_in_token = token[1].split(".")
                data = json.loads(base64.b64decode(id_user_in_token[1]))
                user_identification = data["user_id"]
            else:
                user_identification = None
        except Exception as e:
            user_identification = None
            print("request.META doesn't exist")

        task = get_object_or_404(Task.objects.filter(pk=pk))
        response_data = DetailTaskSerializer(task).data

        for comment in response_data.items():
            if isinstance(comment[1], list):
                if len(comment[1]) > 1:

                    if user_identification:
                        notifics = Notification.objects.filter(task=task.id, user=user_identification)
                        if notifics:
                            for a_notification in notifics:
                                a_notification.seen = True
                                a_notification.save()
        if user_identification:
            notifics = Notification.objects.filter(task=task.id, user=user_identification)
            if notifics:
                for a_notification in notifics:
                    a_notification.seen = True
                    a_notification.save()

        start_time = None
        intervals = TimeTracker.objects.filter(task=task).order_by('-id')
        last_interval = None
        for interval in intervals:
            if not interval.finish_time:
                last_interval = interval
                break

        if last_interval and not last_interval.finish_time:
            start_time = last_interval.start_time
        response_data.update({"start_counter_from": start_time})

        intervals_duration = TimeTracker.objects.filter(task=task)
        duration = 0
        for interval_duration in intervals_duration:
            if interval_duration.duration:
                duration += interval_duration.duration
        response_data.update({"duration": duration})

        return Response(response_data)


# task 5
class UserTaskView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        url_parameters = str(request.META['QUERY_STRING'])
        params = url_parameters.split('&')
        task = None

        for param in params:
            if param:
                key = param.split('=')[0]
                if int(param.split('=')[1]) >= 0:
                    valueStart = (int(param.split('=')[1])) * 10
                    valueEnd = int(valueStart) + 10
                    if key == 'page':
                        task = Task.objects.filter(user_assigned=request.user.id).order_by("-id")[
                               int(valueStart):int(valueEnd)]

                        # there are no task on this page
                        if not task:
                            return Response(status=204)
                else:
                    return Response(status=400)

        if not task:
            task = Task.objects.filter(user_assigned=request.user.id).order_by("-id")[:10]

        return Response(TaskSerializer(task, many=True).data)


# task 5
class UserTaskCreatedView(GenericAPIView):
    serializer_class = TaskSerializer

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        url_parameters = str(request.META['QUERY_STRING'])
        params = url_parameters.split('&')
        task = None

        for param in params:
            if param:
                key = param.split('=')[0]
                if int(param.split('=')[1]) >= 0:
                    valueStart = (int(param.split('=')[1])) * 10
                    valueEnd = int(valueStart) + 10
                    if key == 'page':
                        task = Task.objects.filter(user_created=request.user.id).order_by("-id")[
                               int(valueStart):int(valueEnd)]

                        # there are no task on this page
                        if not task:
                            return Response(status=204)
                else:
                    return Response(status=400)

        if not task:
            task = Task.objects.filter(user_created=request.user.id).order_by("-id")[:10]

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

            if validated_data["status"] == "finished":
                people = []

                if task.user_assigned and request.user != task.user_assigned:
                    people.append(task.user_assigned.id)
                if request.user != task.user_created:
                    people.append(task.user_created.id)

                comments = Comment.objects.filter(task=task)
                for one_comment in comments:
                    if request.user != one_comment.user:
                        people.append(one_comment.user.id)

                people = list(dict.fromkeys(people))
                users = User.objects.filter(pk__in=people)

                for user in users:
                    AddNotificationTaskStatus(user, task, "finished")

                # stop log for this task
                time_finish = TimeTracker.objects.filter(task=task).last()
                if time_finish:
                    time_finish.finish_time = datetime.now()
                    difference = time_finish.finish_time - time_finish.start_time
                    time_finish.duration = (difference.days * 24 * 60 + difference.seconds) / 60
                    time_finish.save()
        else:
            return Response(status=403)

        return Response(TaskSerializer(task).data)


class UpdateTask(GenericAPIView):
    serializer_class = TaskUpdateAllSerializer

    permission_classes = (IsAuthenticated,)

    def put(self, request):
        serializer = TaskUpdateAllSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if request.user == data["user_created"] or request.user == data["user_assigned"]:
                task = Task.objects.get(id=data['id'])
                task.user_created = data["user_created"]
                task.user_assigned = data["user_assigned"]
                task.title = data["title"]
                task.description = data["description"]
                task.status = data["status"]
                task.save()

                if task.user_assigned and task.user_assigned != request.user:
                    AddNotificationTaskStatus(task.user_assigned, task, data["status"])

                response_data = TaskSerializer(task).data
                return Response(response_data)
            else:
                return Response(serializer.errors, status=403)
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

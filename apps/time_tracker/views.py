from datetime import datetime

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, TruncMonth, TruncDay
from django.shortcuts import render
from drf_util.decorators import serialize_decorator
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.utils import json

from apps.task.serializers import TaskSerializer
from apps.time_tracker.serializers import TimeTrackerLogsSerializer, TimeTrackerAddLogSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.time_tracker.models import TimeTracker
from apps.task.models import Task
import datetime
from apps.time_tracker.serializers import UserTimeSerializer, LogDateSerializeer


class TimeTrackerStartView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        task = Task.objects.get(id=pk)

        if TimeTracker.objects.filter(task=task).count() > 0:
            last_interval = TimeTracker.objects.filter(task=task).last()
            if not last_interval.finish_time:
                return Response(status=403)

        if not task:
            return Response(status=404)
        elif task.user_assigned != request.user:
            return Response(status=403)

        time_tracker = TimeTracker.objects.create(
            task=task,
            start_time=datetime.datetime.now(),
        )
        time_tracker.save()

        return Response(status=201)


class TimeTrackerAddLogView(GenericAPIView):
    serializer_class = TimeTrackerAddLogSerializer

    permission_classes = (IsAuthenticated,)

    @serialize_decorator(TimeTrackerAddLogSerializer)
    def post(self, request, pk):
        validated_data = request.serializer.validated_data

        if validated_data['duration'] < 1 or validated_data['duration'] > 1440:
            return Response(status=403)

        task = Task.objects.get(id=pk)

        if not task:
            return Response(status=404)
        elif task.user_assigned != request.user:
            return Response(status=403)

        finish_datetime = datetime.datetime.strptime(str(validated_data['start_time']), '%Y-%m-%d %H:%M:%S.%f')
        finish_datetime = finish_datetime + datetime.timedelta(minutes=validated_data['duration'])

        time_tracker = TimeTracker.objects.create(
            task=task,
            start_time=validated_data['start_time'],
            finish_time=finish_datetime,
            duration=validated_data['duration'],
        )
        time_tracker.save()

        intervals = TimeTracker.objects.filter(task=task)
        duration = 0
        for interval in intervals:
            if interval.duration:
                duration += interval.duration
        task.duration = duration
        task.save()

        return Response(status=201)


# Time Stop! Task2
class TimeTrackerStop(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        task = Task.objects.get(id=pk)

        if not task:
            return Response(status=404)
        elif task.user_assigned != request.user:
            return Response(status=403)

        finish = datetime.datetime.now()
        time_finish = TimeTracker.objects.filter(task=task).order_by('-id')

        for interval in time_finish:
            if not interval.finish_time:
                interval.finish_time = finish
                difference = interval.finish_time - interval.start_time
                interval.duration = (difference.days * 24 * 60 + difference.seconds) / 60
                interval.save()
                break

        intervals = TimeTracker.objects.filter(task=task)
        duration = 0
        for interval in intervals:
            if interval.duration:
                duration += interval.duration
        task.duration = duration
        task.save()

        return Response(status=201)


# Get a list of time logs records by task ID
class TimeTrackerLogsView(GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        time_logs = TimeTracker.objects.filter(task=pk)
        return Response(TimeTrackerLogsSerializer(time_logs, many=True).data)


class TopDurationTimeView(GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        now = datetime.datetime.now()
        last_month = now - datetime.timedelta(days=31)
        tasks = Task.objects.filter(date_create_task__year=last_month.year,
                                    date_create_task__month=last_month.month).order_by('-duration')[:20]

        return Response(TaskSerializer(tasks, many=True).data)


class LoggedTimeView(GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        user = User.objects.filter(id=pk)
        return Response(UserTimeSerializer(user).data)


class LogChartView(GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        tracker = TimeTracker.objects.filter(task__user_assigned=pk).annotate(date=TruncDay('start_time')).values(
            'date').annotate(
            duration=Sum('duration')).values('date', 'duration').order_by('date')
        data = list(tracker)
        return Response(data)


class LogDate(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        url_parameters = str(request.META['QUERY_STRING'])
        params = url_parameters.split('&')
        tracker = None

        for param in params:
            if param and param.split('=')[1] and param.split('=')[0] == "date":
                date_string = param.split('=')[1]
                date = datetime.datetime.strptime(date_string, '%Y-%m-%d')

                tracker = TimeTracker.objects.filter(task__user_assigned=request.user, start_time__year=date.year,
                                                     start_time__month=date.month,
                                                     start_time__day=date.day).order_by("-id")

        return Response(LogDateSerializeer(tracker, many=True).data)


class LogDelete(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        tracker = TimeTracker.objects.filter(pk=pk, task__user_assigned=request.user.id)

        if tracker.count() == 0:
            return Response(status=403)
        tracker.delete()
        return Response(status=204)

from datetime import datetime

from django.shortcuts import render
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView
from apps.time_tracker.serializers import TimeTrackerSerializer, TimeTrackerAddLogSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.time_tracker.models import TimeTracker
from apps.task.models import Task
import datetime
from django.utils.dateparse import parse_date


# class TimeTrackerUserView(GenericAPIView):
#     serializer_class = TimeTrackerSerializer
#
#     permission_classes = (AllowAny,)
#     authentication_classes = ()
#
#     def get(self, request, pk):
#         for task in Task.objects.filter(user_assigned=pk):
#             time_tracker = TimeTracker.objects.filter(task=task.id)
#
#         return Response(TimeTrackerSerializer(time_tracker, many=True).data)


class TimeTrackerStartView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        task = Task.objects.get(id=pk)

        if not task:
            return Response(status=404)
        elif task.user_assigned != request.user:
            return Response(status=403)

        time_tracker = TimeTracker.objects.create(
            task=task,
            start_time=datetime.now(),
        )
        time_tracker.save()

        return Response(status=201)


class TimeTrackerAddLogView(GenericAPIView):
    serializer_class = TimeTrackerAddLogSerializer

    permission_classes = (IsAuthenticated,)

    @serialize_decorator(TimeTrackerAddLogSerializer)
    def post(self, request, pk):
        task = Task.objects.get(id=pk)

        if not task:
            return Response(status=404)
        elif task.user_assigned != request.user:
            return Response(status=403)

        validated_data = request.serializer.validated_data
        finish_datetime = datetime.datetime.strptime(str(validated_data['start_time']), '%Y-%m-%d %H:%M:%S.%f')
        finish_datetime = finish_datetime + datetime.timedelta(minutes=validated_data['duration'])

        time_tracker = TimeTracker.objects.create(
            task=task,
            start_time=validated_data['start_time'],
            finish_time=finish_datetime,
            duration=validated_data['duration'],
        )
        time_tracker.save()

        return Response(status=201)

#Time Stop! Task2
class TimeTrackerStop(GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def put(self, request, pk):
        task = Task.objects.get(id=pk)
        finish = datetime.now()
        time_finish = TimeTracker.objects.filter(task=task).first()
        if time_finish:
            time_finish.finish_time = finish
            time_finish.save()

        return Response(status=201)

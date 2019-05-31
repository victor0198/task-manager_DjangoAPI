from datetime import datetime

from django.shortcuts import render
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView
from apps.time_tracker.serializers import TimeTrackerSerializer, TimeTrackerStartSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.time_tracker.models import TimeTracker
from apps.task.models import Task


class TimeTrackerView(GenericAPIView):
    serializer_class = TimeTrackerSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        time_tracker = TimeTracker.objects.filter(task=pk)
        return Response(TimeTrackerSerializer(time_tracker, many=True).data)


class TimeTrackerStartView(GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        time_tracker = TimeTracker.objects.create(
            task=task,
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

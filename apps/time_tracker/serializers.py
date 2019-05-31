from apps.task.models import Task
from apps.time_tracker.models import TimeTracker
from rest_framework import serializers


class TimeTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTracker
        fields = ('task', 'start_time', 'finish_time', 'duration')

class TimeTrackerStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTracker
        fields = ('task', 'start_time', 'finish_time', 'duration')


class TimeTrackerLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTracker
        fields = ('start_time', 'finish_time', 'duration')

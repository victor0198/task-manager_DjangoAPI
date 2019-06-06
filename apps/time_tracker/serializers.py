from apps.time_tracker.models import TimeTracker
from rest_framework import serializers


class TimeTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTracker
        fields = '__all__'


class TimeTrackerAddLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTracker
        fields = ('start_time', 'duration')


class TimeTrackerLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTracker
        fields = ('start_time', 'finish_time', 'duration')




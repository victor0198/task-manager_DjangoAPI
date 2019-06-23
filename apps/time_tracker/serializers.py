import datetime

from django.db.models import Sum

from apps.time_tracker.models import TimeTracker
from rest_framework import serializers
from apps.task.models import Task
from django.contrib.auth.models import User
from apps.task.serializers import TaskSearchSerializer


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


class UserTimeSerializer(serializers.ModelSerializer):
    logged_minutes = serializers.SerializerMethodField()

    def get_logged_minutes(self, obj):
        now = datetime.datetime.now()
        last_month = now - datetime.timedelta(days=31)
        user = User.objects.get(username=obj[0])
        return Task.objects.filter(date_create_task__year=last_month.year, date_create_task__month=last_month.month,
                                   user_assigned=user).aggregate(Sum('duration'))['duration__sum']

    class Meta:
        model = Task
        fields = ('logged_minutes',)


class LogDateSerializeer(serializers.ModelSerializer):
    task = serializers.SerializerMethodField()

    def get_task(self, obj):
        return TaskSearchSerializer(obj.task).data

    class Meta:
        model = TimeTracker
        fields = '__all__'

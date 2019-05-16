from rest_framework import serializers
from apps.task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "description", "status", "user_created")
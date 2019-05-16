from rest_framework import serializers

from apps.task.models import Notification, Task
from apps.task.serializers import TaskSerializer


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


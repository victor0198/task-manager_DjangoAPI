from rest_framework import serializers

from apps.notification.models import Notification
from apps.task.serializers import TaskSerializer


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


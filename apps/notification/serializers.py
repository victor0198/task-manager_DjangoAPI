from flex.exceptions import ValidationError
from rest_framework import serializers

from apps.comment.models import Comment
from apps.notification.models import Notification
from apps.task.models import Task


class CommentTaskSerializer(serializers.ModelSerializer):
    task = serializers.SerializerMethodField()

    def get_task(self, obj):
        return {'title': obj.task.title, 'id': obj.task.id}

    class Meta:
        model = Comment
        fields = ['task']


class NotificationSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()

    @staticmethod
    def get_comment(obj):
        noti = Notification.objects.get(id=obj.id)
        comment = Comment.objects.filter(task=obj.task.id).first()
        return CommentTaskSerializer(comment).data

    class Meta:
        model = Notification
        fields = ['id', 'user', 'task', 'seen', 'comment']






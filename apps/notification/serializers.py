from flex.exceptions import ValidationError
from rest_framework import serializers

from apps.comment.models import Comment
from apps.notification.models import Notification
from apps.task.models import Task


class CommentTaskSerializer(serializers.ModelSerializer):
    taskk = serializers.SerializerMethodField()

    def get_taskk(self, obj):
        return {'task_name': obj.task.title, 'task_id': obj.task.id}

    class Meta:
        model = Comment
        fields = ['taskk']


class NotificationSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    task = serializers.SerializerMethodField()

    @staticmethod
    def get_comment(obj):
        noti = Notification.objects.get(id=obj.id)
        comment = Comment.objects.filter(task=obj.task.id).first()
        return CommentTaskSerializer(comment).data

    def get_task(self, obj):
        return {'task_id': obj.task.id, 'task_title': obj.task.title, 'task_status': obj.task.status}

    class Meta:
        model = Notification
        fields = ['id', 'user', 'task', 'seen', 'comment']

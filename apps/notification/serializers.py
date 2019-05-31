from flex.exceptions import ValidationError
from rest_framework import serializers

from apps.comment.models import Comment
from apps.notification.models import Notification
from apps.task.models import Task


class CommentTaskSerializer(serializers.ModelSerializer):
    task = serializers.SerializerMethodField()

    def get_task(self, obj):
        if obj.task.status == "created":

            return {'title': obj.task.title, 'id': obj.task.id}
        else:
            return {}

    class Meta:
        model = Comment
        fields = ['task']


class NotificationSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()

    @staticmethod
    def get_comment(obj):
        comment = Comment.objects.filter(task=obj.task.id).first()
        return CommentTaskSerializer(comment).data

    def get_task(self, obj):
        return {'id': obj.task.id, 'title': obj.task.title, 'status': obj.task.status}

    class Meta:
        model = Notification
        fields = ['id', 'user', 'task', 'seen', 'comment', 'status']

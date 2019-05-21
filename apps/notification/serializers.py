from flex.exceptions import ValidationError
from rest_framework import serializers

from apps.comment.models import Comment
from apps.notification.models import Notification


class CommentTaskSerializer(serializers.ModelSerializer):
    task = serializers.SerializerMethodField()

    def get_task(self, obj):
        return {'task_name': obj.task.title, 'task_id':obj.task.id}

    class Meta:
        model = Comment
        fields = ['task']


class NotificationSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()

    @staticmethod
    def get_comment(obj):
        comment = Comment.objects.filter(task=obj.id).first()
        return CommentTaskSerializer(comment).data

    class Meta:
        model = Notification
        fields = ['id', 'user', 'task', 'seen', 'comment']






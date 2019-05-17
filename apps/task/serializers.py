from rest_framework import serializers
from apps.task.models import Task
from apps.comment.models import Comment
from rest_framework.exceptions import ValidationError


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "description", "status", "user_created")


# --------Comments
class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'text']


class DetailTaskSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = Comment.objects.filter(task=obj.id)
        return CommentsSerializer(comments, many=True).data

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'comments']


class TaskUpdateStatus(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def validate_id(self, value):
        post = Task.objects.filter(id=value).first()
        if not post:
            raise ValidationError("Not exists")
        return value

    class Meta:
        model = Task
        fields = ['id']


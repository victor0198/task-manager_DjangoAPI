from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.comment.models import Comment
from apps.task.models import Task
from django.contrib.auth.models import User
from apps.users.serializers import UserSerializer, UserTaskSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'user_assigned')


class TaskSerializerCreateResponse(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description')


class TaskSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "description", "status")


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


class FilterTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('status', 'user_assigned', 'title')


class MyFilterSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    status = serializers.CharField(max_length=10, required=False)
    user_assigned = serializers.IntegerField(required=False)


class TaskCommentsSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    @staticmethod
    def get_comments(obj):
        comments = Comment.objects.filter(task=obj.id)
        return CommentsSerializer(comments, many=True).data

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'user_created', 'user_assigned', "comments"]

class TaskUpdateAllSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def validate_id(self, value):
        task = Task.objects.filter(id=value).first()
        if not task:
            raise ValidationError("Not exists")
        return value

    class Meta:
        model = Task
        fields = ["id", "user_created", "user_assigned", "title", "description", "status"]
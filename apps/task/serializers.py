from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.comment.models import Comment
from apps.task.models import Task
from django.contrib.auth.models import User
from apps.users.serializers import UserSerializer, UserTaskSerializer


class TaskSerializer(serializers.ModelSerializer):
    user_assigned = serializers.SerializerMethodField()
    user_created = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_user_created(self, obj):
        return {"username": obj.user_created.username, "id": obj.user_created.id}

    def get_user_assigned(self, obj):
        return {"username": obj.user_created.username, "id": obj.user_created.id}

    @staticmethod
    def get_comments(obj):
        comments = Comment.objects.filter(task=obj.id).count()
        return {"count_comment": comments}

    class Meta:
        model = Task
        fields = '__all__'


class TaskSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'user_assigned', 'date_create_task')


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
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = User.objects.filter(id=obj.user.id).first()
        return {"id": user.id, "username": user.username}

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'date_create_comment']


# ------------------------------------------------------------------------------
class DetailTaskSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    user_assigned = serializers.SerializerMethodField()
    user_created = serializers.SerializerMethodField()

    def get_user_created(self, obj):
        return {"username": obj.user_created.username, "id": obj.user_created.id}

    def get_user_assigned(self, obj):
        if obj.user_assigned:
            return {"username": obj.user_assigned.username, "id": obj.user_assigned.id}
        else:
            return None

    def get_comments(self, obj):
        comments = Comment.objects.filter(task=obj.id).order_by('-id')
        return CommentsSerializer(comments, many=True).data

    class Meta:
        model = Task

        fields = ['id', 'title', 'description', 'status', 'comments', 'user_created', 'user_assigned',
                  'date_create_task', 'update_task']


class FilterTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('status', 'user_assigned', 'title')


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


class TaskSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title')


class TaskUpdateStateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def validate_id(self, value):
        task = Task.objects.filter(id=value).first()
        if not task:
            raise ValidationError("Not exists")
        return value

    class Meta:
        model = Task
        fields = ('id', 'status')

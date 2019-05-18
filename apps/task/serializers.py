from rest_framework import serializers
from apps.comment.models import Comment
from apps.task.models import Task



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'user_assigned')


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

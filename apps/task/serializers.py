from rest_framework import serializers
<<<<<<< HEAD
from apps.task.models import Task
=======

from apps.task.models import Comment, Task, Notification
>>>>>>> origin/st_vi


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "description", "status", "user_created")
<<<<<<< HEAD

from apps.task.models import Comment, Task, Notification


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
=======

>>>>>>> origin/st_vi

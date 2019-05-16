from rest_framework import serializers

from apps.task.models import Comment, Task, Notification


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
<<<<<<< HEAD
        fields = '__all__'
=======
        fields = '__all__'


class TaskSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "description", "status", "user_created")
>>>>>>> victor0198

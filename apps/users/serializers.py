from django.contrib.auth.models import User
from rest_framework import serializers
from apps.task.models import Task


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password",)


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")


class UserSpentTimeSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    def get_duration(self, obj):
        minutes = 0
        for task in Task.objects.filter(user_assigned=obj.id):
            minutes += task.duration
        print(minutes)
        return minutes

    class Meta:
        model = User
        fields = ('duration',)

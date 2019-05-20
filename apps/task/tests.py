from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APIClient
from rest_framework import (
    HTTP_HEADER_ENCODING, RemovedInDRF310Warning, authentication, generics,
    permissions, serializers, status, views
)
from django.test import TestCase

from apps.task.models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        response = self.client.post(reverse('token_register'), {
            "first_name": "string",
            "last_name": "string",
            "username": "string",
            "password": "string"
        })
        self.assertEqual(response.status_code, 200)
        self.user = User.objects.filter(username='string').first()
        self.assertIsNotNone(self.user)

        print(User.objects.filter(username='string').count())

        self.client.force_authenticate(self.user)

    # Task 3: View list of tasks, TEST
    def test_task_list(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)

    # Task 6: View Completed tasks , TEST
    def test_task_completed_list(self):
        response = self.client.get(reverse('completed_list'))
        self.assertEqual(response.status_code, 200)

    # TEST test with permission_classes = (IsAuthenticated,)
    def test_task_create(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.assertIsNotNone(self.id)

        response = self.client.post(reverse('task_create'), {
            "title": "string",
            "description": "string",
            "status": "created",
            "user_assigned": 0
        })
        self.assertEqual(response.status_code, 200)

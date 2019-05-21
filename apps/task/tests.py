from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from django.test import TestCase
from apps.task.models import Task

class AnimalTestCase(TestCase):
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

    def test_task_list(self):
        response = self.client.get(reverse('completed_list'))
        self.assertEqual(response.status_code, 200)

    def test_task_completed_list(self):

        response = self.client.get(reverse('completed_list'))
        print(response.data)
        self.assertEqual(Task.is_finished(response), True)

        self.assertEqual(response.status_code, 200)

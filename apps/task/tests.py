from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient, APIRequestFactory
from django.test import TestCase


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
        response = self.client.get('/task/tasks_all/')
        self.assertEqual(response.status_code, 200)

    def test_task_completed_list(self):
        response = self.client.get(reverse('completed_list'))
        self.assertEqual(response.status_code, 200)


client = APIClient(enforce_csrf_checks=True)
client.post('/comments/create/', {'text': 'new idea'}, format='json')

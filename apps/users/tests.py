from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from django.test import TestCase
from apps.task.models import Task
# Create your tests here.

class TaskTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        response = self.client.post(reverse('token_register'), {
            "first_name": "string",
            "last_name": "string",
            "username": "string",
            "password": "string"
        })
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.user = User.objects.filter(username='string').first()
        self.assertIsNotNone(self.user)

        print(User.objects.filter(username='string').count())


        self.client.force_authenticate(self.user)

    #
    # def test_meDetails(self):
    #     self.client = APIClient()
    #     self.client.force_authenticate(self.user)
    #     self.assertIsNotNone(self.user)
    #
    #     response = self.client.get(reverse('user_me'))
    #     print(response.data)
    #     self.assertEquals(response.data, 200)
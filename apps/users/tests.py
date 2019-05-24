from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory
from apps import users
from apps.users import views
from apps.task import views
from apps.notification import views
from apps.comment import views
from apps.common import views

from django.test import TestCase
from apps.task.models import Task
# Create your tests here.
from apps.users.views import UserSearchViewSet


class TaskTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        response = self.client.post(reverse('token_register'), {
            "first_name": "test_first_name_1",
            "last_name": "test_last_name_1",
            "username": "test_username_1",
            "password": "test_password_1"
        })
        self.assertEqual(response.status_code, 200)
        self.user = User.objects.filter(username='test_username_1').first()
        self.assertIsNotNone(self.user)

        self.client.force_authenticate(self.user)

    def test_user_search(self):
        print("--user_search--start")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)
        response = self.client.get(reverse('user_me'))
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        print("--user_search--end")
        print("")

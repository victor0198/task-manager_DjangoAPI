from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from django.test import TestCase

from apps.comment.models import Comment
from apps.notification.views import AddNotificationComment


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

        self.client.force_authenticate(self.user)

    def test_comment_create(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)

        response = self.client.post(reverse('comment_create'), AddNotificationComment(user=Comment.user, comment=1), {

            "task": 1,
            "text": "string",

        })

        print(response.data)

        # print(self.user)
        self.assertEqual(response.status_code, 200)

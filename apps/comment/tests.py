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

        comment = self.client.post(reverse('comment_create'), {

            "task": 1,
            "text": "string",

        })

        print(comment.data)

        # print(self.user)
        self.assertEqual(comment.status_code, 200)

    # test delete a task

    def test_comment_delete(self):
        print("--delete comment--start")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)
        response0 = self.client.post(reverse('task_create'), {
            "title": "string",
            "description": "string",
            "status": "created",
            "user_assigned": 1,
            "text": "string",
            "task": 1,
        })
        response1 = self.client.post(reverse('comment_create'), {
            "task": 1,
            "text": "string"
        })
        response2 = self.client.delete(reverse('delete_task', args=(1,)))
        print(response0.status_code)
        print(response1.status_code)
        print(response2.status_code)

        self.assertEqual(response2.status_code, 204)
        print("--delete task--end")
        print("")

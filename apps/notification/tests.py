from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from apps.comment.models import Comment
from apps.notification.models import Notification
from apps.notification.views import AddNotificationComment, AddNotificationTask, AddNotificationTaskClosed
from apps.task.models import Task


class NotificationTestCase(TestCase):
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

        # print(User.objects.filter(username='string').count())

        self.client.force_authenticate(self.user)

    def test_myNotification(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse('my_notification'))
        self.assertEquals(response.status_code, 200)

    def test_commentNotification(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)

        response = self.client.post(AddNotificationComment(user=Comment.user, comment=1), {
            "user": 1,
            "seen": False,
        })

    def test_ClosedNotification(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)

        response = self.client.post(AddNotificationTaskClosed(user=1, task=1), {
            "user": 1,
            "seen": False,
        })
        # print(response.data)
        print(self.user)

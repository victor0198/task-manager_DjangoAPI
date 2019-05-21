from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from django.test import TestCase
from django.contrib.auth.decorators import login_required


# Create your tests here.
# TEST test with permission_classes = (IsAuthenticated,)
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

    @login_required
    def test_task_create(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        comment = self.client.post(reverse('comment_create'), {

            "task": 0,
            "text": "string",

        })
        print(comment.data)
        self.assertEqual(comment.status_code, 200)

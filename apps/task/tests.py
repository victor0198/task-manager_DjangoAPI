from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.generics import get_object_or_404
from rest_framework.test import APIClient, APIRequestFactory

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
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.user = User.objects.filter(username='string').first()
        self.assertIsNotNone(self.user)

        print(User.objects.filter(username='string').count())

        self.client.force_authenticate(self.user)

    # Task 3: View list of tasks, TEST
    def test_task_list(self):
        response = self.client.get(reverse('completed_list'))
        self.assertEqual(response.status_code, 200)

    # Task 6: View Completed tasks , TEST
    def test_task_completed_list(self):
        response = self.client.get(reverse('completed_list'))
        self.assertEqual(response.status_code, 200)

    """
            THIS TEST DONT WORKS 
    """

    # task 4: Create a task

    def test_task_create(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.assertIsNotNone(self.user)

        response = self.client.post(reverse('task_create'), {
            "title": "string",
            "description": "string",
            "status": "created",
            "user_assigned": 1,
            "text": "string",
            "task": 1,
        })
        print(response.data)
        print(self.user)
        self.assertEqual(response.status_code, 200)

    # TEST test with permission_classes = (IsAuthenticated,)

    # # delete task
    #
    # def test_task_delete(self):
    #     self.client = APIClient()
    #     self.client.force_authenticate(user=self.user)
    #     self.assertIsNotNone(self.user)
    #
    #     response = self.client.delete(reverse('delete_task', args=1))
    #     print(response.data)
    #     self.assertEquals(response.status_code, 204)

    def test_finish_task(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)

        response = self.client.put(reverse('finish_task', args=(1,)))
        print(response.data)
        self.assertEquals(response.status_code, 200)

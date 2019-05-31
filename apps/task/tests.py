from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APIClient

from django.test import TestCase

from apps import task
from apps.task.models import Task
from apps.notification.models import Notification
from apps.task.serializers import TaskSerializer
from apps.common import views


class TaskTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        response = self.client.post(reverse('token_register'), {
            "first_name": "test_first_name_1",
            "last_name": "test_last_name_1",
            "username": "test_username_1",
            "password": "test_password_1"
        })
        self.assertEqual(response.status_code, 201)

        response = self.client.post(reverse('token_register'), {
            "first_name": "test_first_name_2",
            "last_name": "test_last_name_2",
            "username": "test_username_2",
            "password": "test_password_2"
        })
        self.assertEqual(response.status_code, 201)

        self.user = User.objects.filter(username='test_username_1').first()
        self.assertIsNotNone(self.user)
        self.client.force_authenticate(self.user)

    # create task
    def test_task_create(self):
        print("--create task--start")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)
        response = self.client.post(reverse('task_create'), {
            "title": "string",
            "description": "string",
            "user_assigned": 1,
        })
        print(response.status_code)
        self.assertEqual(response.status_code, 201)
        print("--create task--end")
        print("")

    # crate task for yourself - not used yet, because there isn't personal page
    def test_task_create_self(self):
        print("--create task self--start")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)
        response = self.client.post(reverse('task_create_self'), {
            "title": "test_self_task",
            "description": "test_self_desc",
            "status": "created"
        })
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        print("--create task self--end")
        print("")

    # get my tasks
    def test_task_get_mine(self):
        print("--create task--start")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)
        response1 = self.client.post(reverse('task_create'), {
            "title": "string",
            "description": "string",
            "user_assigned": 1,
        })
        response2 = self.client.get(reverse('all_task_user'))
        print(response1.status_code)
        print(response2.status_code)
        self.assertEqual(response2.status_code, 200)
        print("--create task--end")
        print("")

    # UpdateTask by id
    def test_task_update(self):
        print("--update task--start")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)
        response1 = self.client.post(reverse('task_create'), {
            "title": "string",
            "description": "string",
            "user_assigned": 1,
        })
        response2 = self.client.put(reverse('update_task'), {
            "id": 1,
            "user_created": 1,
            "user_assigned": 1,
            "title": "updated_title",
            "description": "updated_description",
            "status": "finished"
        })

        print(response1.status_code)
        print(response2.status_code)

        self.assertEqual(response2.status_code, 200)
        print("--update task--end")
        print("")

    # update task status
    def test_task_update_status(self):
        print("--update task status--start")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)
        response1 = self.client.post(reverse('task_create'), {
            "title": "string",
            "description": "string",
            "user_assigned": 1,
        })
        response2 = self.client.put(reverse('update_status'), {
            "id": 1,
            "status": "finished"
        })

        print(response1.status_code)
        print(response2.status_code)

        self.assertEqual(response2.status_code, 200)
        print("--update task status--end")
        print("")

    # try to update with invalid data
    def test_task_update_invalid_serializer(self):
        print("--update task invalid_serializer--start")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)
        response1 = self.client.post(reverse('task_create'), {
            "title": "string",
            "description": "string",
            "user_assigned": 1,
        })
        response2 = self.client.put(reverse('update_task'), {
            "id": 1,
            "user_creat": 1,
            "user_assign": 1,
            "title": "updated_title",
            "description": "updated_description",
            "status": "finished"
        })

        print(response1.status_code)
        print(response2.status_code)
        self.assertEqual(response2.status_code, 400)
        print("--update task invalid_serializer--end")
        print("")

    # get list of completed tasks
    def test_task_completed_list(self):
        print("--list of completed tasks--start")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)
        response1 = self.client.post(reverse('task_create'), {
            "title": "string",
            "description": "string",
            "user_assigned": 1,
        })
        response2 = self.client.put(reverse('update_task'), {
            "id": 1,
            "user_created": 1,
            "user_assigned": 1,
            "title": "updated_title",
            "description": "updated_description",
            "status": "finished"
        })
        response3 = self.client.get(reverse('completed_list'))
        print(response1.status_code)
        print(response2.status_code)
        print("-got tasks--")
        print(response3.json())
        print("--checking for completed status--")
        for task in response3.json():
            task_object = Task.objects.filter(id=task["id"]).first()
            print(str(task["id"]) + " : " + str(
                "OK" if Task.is_finished(task_object) else ("Wrong status: " + Task.get_status(task_object))))
        self.assertEqual(response3.status_code, 200)
        print("--list of completed tasks--end")
        print("")

    # delete a task
    def test_task_delete(self):
        print("--delete task--start")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)
        response1 = self.client.post(reverse('task_create'), {
            "title": "string",
            "description": "string",
            "user_assigned": 1,
        })
        response2 = self.client.delete(reverse('delete_task', args=(1,)))
        print(response1.status_code)
        print(response2.status_code)

        self.assertEqual(response2.status_code, 204)
        print("--delete task--end")
        print("")

    # try to delete a task that doesn't exist
    def test_task_delete_not_exist(self):
        print("--delete task not_exist--start")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)
        response1 = self.client.post(reverse('task_create'), {
            "title": "string",
            "description": "string",
            "user_assigned": 1,
        })
        response2 = self.client.delete(reverse('delete_task', args=(2,)))
        print(response1.status_code)
        print(response2.status_code)

        self.assertEqual(response2.status_code, 403)
        print("--delete task not_exist--end")
        print("")

    # get one task with all comments
    def test_task_get_with_comments(self):
        print("--get task with comments--start")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)
        response1 = self.client.post(reverse('task_create'), {
            "title": "string",
            "description": "string",
            "user_assigned": 1,
        })
        print(response1.status_code)
        response2 = self.client.post(reverse('comment_create'), {
            "task": 1,
            "text": "test_comment1"
        })
        print(response2.status_code)
        response2 = self.client.post(reverse('comment_create'), {
            "task": 1,
            "text": "test_comment2"
        })
        print(response2.status_code)
        response3 = self.client.get(reverse('tasks_all_details', args=(1,)))
        print(response3.status_code)
        task_got = dict(response3.json())
        print("-comments-")
        for comment in task_got['comments']:
            print(str(comment['id']) + " : " + str(comment))
        self.assertEqual(response2.status_code, 200)
        print("--get task with comments--end")
        print("")

    # send notifications to all who commented
    def test_task_create_notification(self):
        print("--create task--start")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.assertIsNotNone(self.user)
        print("1) adding task as user1")
        response1 = self.client.post(reverse('task_create'), {
            "title": "string",
            "description": "string",
            "user_assigned": 2,
        })
        if response1.status_code == 201:
            print("task added as user1")
        self.user = User.objects.filter(username='test_username_2').first()
        self.assertIsNotNone(self.user)
        self.client.force_authenticate(self.user)
        print("2) adding comment as user2")
        response2 = self.client.post(reverse('comment_create'), {
            "task": 1,
            "text": "test_comment1"
        })
        if response2.status_code == 200:
            print("comment added as user2")
        self.user = User.objects.filter(username='test_username_1').first()
        self.assertIsNotNone(self.user)
        self.client.force_authenticate(self.user)
        print("3) changing status to finish as user1")
        response3 = self.client.put(reverse('update_status'), {
            "id": 1,
            "status": "finished"
        })
        if response3.status_code == 200:
            print("status updated as user1")
        print("")
        print("Notification for user1 : " + str(
            Notification.objects.filter(user=User.objects.filter(username="test_username_1").first())))
        print("Notification for user2 : " + str(
            Notification.objects.filter(user=User.objects.filter(username="test_username_2").first())))

        # # get token of user1
        # response4 = self.client.post(reverse('token_obtain_pair'), {
        #     "username": 'test_username_1',
        #     "password": "test_password_1"
        # })
        # print(response4.json()['access'])
        # # change seen value of notification to true
        # secret = 'Bearer ' + str(response4.json()['access'])
        # response5 = self.client.get(reverse('tasks_all_details', args=(1,)))

        print(response3.status_code)
        self.assertEqual(response3.status_code, 200)
        print("--create task--end")
        print("")

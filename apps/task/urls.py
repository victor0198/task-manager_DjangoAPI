from django.urls import path
from apps.task.views import TaskListView, CompletedTaskListView, DeleteView, AddTaskView, AddTaskSelfView, FinishTask, \
    TaskCommentsView, UserTaskView, FilterTask, TaskItemCommentsView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns += [

    path('tasks_all/', TaskListView.as_view(), name='task_list'),
    path('completed_task/', CompletedTaskListView.as_view(), name='completed_list'),
    path('delete_task/<int:pk>/', DeleteView.as_view(), name='delete_task'),
    path('create/', AddTaskView.as_view(), name='task_create'),
    path('create_self/', AddTaskSelfView.as_view(), name='task_create_self'),
    path('task_details/<int:pk>/', TaskItemCommentsView.as_view(), name='task_item'),

    path('task_comments_all/<int:pk>/', TaskCommentsView.as_view(), name='all_commnets'),
    path('my_tasks/', UserTaskView.as_view(), name='all_task_user'),
    path('task_finish/<int:pk>', FinishTask.as_view(), name="finish_task"),
    path('task_all_filter/', FilterTask.as_view(), name="filter_task"),

]

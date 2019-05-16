from django.urls import path
<<<<<<< HEAD

from rest_framework.routers import DefaultRouter
from apps.task.views import  AddTaskSelfView

router = DefaultRouter()

from apps.task.views import AddTaskView, TaskListView, CompletedTaskListView, DeleteView
=======

from apps.task.views import TaskListView, CompletedTaskListView, DeleteView, AddTaskView, AddTaskSelfView
>>>>>>> origin/st_vi
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register(r'tasks', TaskViewSet, basename='task')
<<<<<<< HEAD
=======

>>>>>>> origin/st_vi

urlpatterns = router.urls

urlpatterns += [
<<<<<<< HEAD
    path('create/', AddTaskView.as_view(), name='task_create'),
    path('create_self/', AddTaskSelfView.as_view(), name='task_create_self'),
=======

>>>>>>> origin/st_vi
    path('task/', TaskListView.as_view(), name='task_list'),
    path('completed_task/', CompletedTaskListView.as_view(), name='completed_list'),
    path('delete_task/<int:pk>/', DeleteView.as_view(), name='delete_task'),

<<<<<<< HEAD
=======
    path('create/', AddTaskView.as_view(), name='task_create'),
    path('create_self/', AddTaskSelfView.as_view(), name='task_create_self'),

>>>>>>> origin/st_vi
]

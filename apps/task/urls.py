from django.urls import path
<<<<<<< HEAD
from apps.task.views import TaskListView, CompletedTaskListView, DeleteView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'tasks', TaskViewSet, basename='task')
=======
from rest_framework.routers import DefaultRouter
from apps.task.views import AddTaskView, AddTaskSelfView

router = DefaultRouter()
>>>>>>> victor0198

urlpatterns = router.urls

urlpatterns += [
<<<<<<< HEAD
    path('task/', TaskListView.as_view(), name='task_list'),
    path('completed_task/', CompletedTaskListView.as_view(), name='completed_list'),
    path('delete_task/<int:pk>/', DeleteView.as_view(), name='delete_task'),
=======
    path('create/', AddTaskView.as_view(), name='task_create'),
    path('create_self/', AddTaskSelfView.as_view(), name='task_create_self'),

>>>>>>> victor0198
]

from django.urls import path
from apps.task.views import TaskListView, CompletedTaskListView, DeleteView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = router.urls

urlpatterns += [
    path('task/', TaskListView.as_view(), name='task_list'),
    path('completed_task/', CompletedTaskListView.as_view(), name='completed_list'),
    path('delete_task/<int:pk>/', DeleteView.as_view(), name='delete_task'),
]

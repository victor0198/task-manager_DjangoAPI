from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.task.views import TaskCommentsView, UserTaskView, TaskViewSet, FinishTask

router = DefaultRouter()
router.register(r'task', TaskViewSet, basename='task_list')
urlpatterns = router.urls

urlpatterns += [
path('task_comments_all/<int:pk>/',TaskCommentsView.as_view(), name='all_commnets'),
path('task_user_all/<int:pk>/',UserTaskView.as_view(), name='all_task_user'),
path('task_finish/',FinishTask.as_view(), name = "finish_task")
]

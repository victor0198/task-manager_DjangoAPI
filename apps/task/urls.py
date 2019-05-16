from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.task.views import AddTaskView, AddTaskSelfView

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('create/', AddTaskView.as_view(), name='task_create'),
    path('create_self/', AddTaskSelfView.as_view(), name='task_create_self'),

]

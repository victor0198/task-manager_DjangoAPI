from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.time_tracker.views import TimeLogsListView

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('time_list_logs_view/<int:pk>/', TimeLogsListView.as_view(), name='time_logs'),
]


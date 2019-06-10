from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.time_tracker.views import LogDate, LogDelete

router = DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('logs_on_date/', LogDate.as_view(), name='logs_on_date'),
    path('delete/<int:pk>/', LogDelete.as_view(), name='logs_on_date'),
]


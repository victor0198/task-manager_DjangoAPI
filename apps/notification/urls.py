from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.notification.views import MyNotificationSerializer

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('my_notification/<int:pk>/', MyNotificationSerializer.as_view(), name='my_notification'),

]

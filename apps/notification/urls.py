from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.notification.views import MyNotificationView,CountNewNotifications

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('my_notification/<int:pk>/', MyNotificationView.as_view(), name='my_notification'),
    path('count_new_notification/', CountNewNotifications.as_view(), name='count_notifications_new'),

]

from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.notification.views import MyNotificationView

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('my_notification/', MyNotificationView.as_view(), name='my_notification'),
    # path('list_notification/', MyNotificationView.as_view(), name='list_notifications_new'),

]

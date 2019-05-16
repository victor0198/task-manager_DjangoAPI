from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.comment.views import AddCommentView

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('create/', AddCommentView.as_view(), name='task_create'),

]

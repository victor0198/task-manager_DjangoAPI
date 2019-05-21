from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.comment.views import AddCommentView

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('create_comment/', AddCommentView.as_view(), name='comment_create'),

]

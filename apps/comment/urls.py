from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.comment.views import AddCommentView, DeleteCommentView

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('create_comment/', AddCommentView.as_view(), name='comment_create'),
    path('delete_comment/<int:pk>/', DeleteCommentView.as_view(), name='comment_delete'),

]

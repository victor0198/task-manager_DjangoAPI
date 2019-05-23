from datetime import datetime

from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.comment.serializers import CommentsSerializer, CommentSerializer
from apps.notification.views import AddNotificationComment
from apps.comment.models import Comment

# task 10
from apps.task.models import Task


class AddCommentView(GenericAPIView):
    serializer_class = CommentsSerializer

    permission_classes = (IsAuthenticated,)

    @serialize_decorator(CommentsSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        comment = Comment.objects.create(
            task=validated_data['task'],
            user=request.user,
            text=validated_data['text'],
        )
        task = Task.objects.get(id=comment.task.id)
        task.update_task = datetime.now()
        task.save()
        comment.save()

        if request.user != comment.task.user_assigned:
            AddNotificationComment(comment.task.user_assigned, comment, task)
        if request.user != comment.task.user_created:
            AddNotificationComment(comment.task.user_created, comment, task)

        return Response(CommentSerializer(comment).data)

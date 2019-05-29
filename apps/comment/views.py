from datetime import datetime
from django.contrib.auth.models import User
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

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

        people = []

        if comment.task.user_assigned and request.user != comment.task.user_assigned:
            people.append(comment.task.user_assigned.id)
        if request.user != comment.task.user_created:
            people.append(comment.task.user_created.id)

        comments = Comment.objects.filter(task=task)
        for one_comment in comments:
            if request.user != one_comment.user:
                people.append(one_comment.user.id)

        people = list(dict.fromkeys(people))

        users = User.objects.filter(pk__in=people)

        for user in users:
            print("notification to " + str(user))
            AddNotificationComment(user, comment, task)

        return Response(CommentSerializer(comment).data)


# delete comment
class DeleteCommentView(GenericAPIView):
    serializer_class = CommentsSerializer

    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        comment = Comment.objects.filter(pk=pk, user=request.user.id).first()
        if not comment:
            return Response(status=404)
        comment.delete()
        return Response(status=HTTP_204_NO_CONTENT)
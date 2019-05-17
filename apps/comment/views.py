from django.shortcuts import render
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.comment.serializers import CommentSerializer
from apps.notification.views import AddNotificationComment
from apps.comment.models import Comment


class AddCommentView(GenericAPIView):
    serializer_class = CommentSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(CommentSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        comment = Comment.objects.create(
            task=validated_data['task'],
            user=validated_data['user'],
            text=validated_data['text'],
        )
        comment.save()

        AddNotificationComment(comment.user, comment)

        return Response(CommentSerializer(comment).data)

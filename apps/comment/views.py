from django.shortcuts import render
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from apps.task.models import Comment
from rest_framework.response import Response
from apps.comment.serializers import CommentSerializer


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

        return Response(CommentSerializer(comment).data)

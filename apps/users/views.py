# Create your views here.
from django.contrib.auth.models import User
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from apps.users.serializers import UserSearchSerializer, UserSerializer
from rest_framework import filters


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(UserSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            is_superuser=False,
            is_staff=False
        )
        user.set_password(validated_data['password'])
        user.save()

        return Response(UserSerializer(user).data)


class UserSearchViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    serializer_class = UserSearchSerializer
    queryset = User.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('^username',)

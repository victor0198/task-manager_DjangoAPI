from django.contrib.auth.models import User
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from apps.users.serializers import UserSearchSerializer, UserSerializer, UserMeSerializer, UserSpentTimeSerializer
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

        return Response(UserSerializer(user).data, status=201)


class UserSearchViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    serializer_class = UserSearchSerializer
    queryset = User.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('^username',)
    http_method_names = ['get']


class MeDetails(GenericAPIView):
    serializer_class = UserMeSerializer

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()

        return Response(UserMeSerializer(user).data)


class UserSpentTimeView(APIView):
    serializer_class = UserSpentTimeSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        return Response(UserSpentTimeSerializer(user).data)

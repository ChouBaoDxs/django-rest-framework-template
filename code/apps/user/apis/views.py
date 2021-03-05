from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, ValidationError, MethodNotAllowed
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from user.apis.serializers import (
    UserMeSerializer,
    UserProfileModelSerializer,
    UserProfileDisplaySerializer,
    UserProfileCreateOrUpdateSerializer
)
from user.models import UserProfile
from utils.mixins import SerializerMixin, PermissionMixin
from .schemas import UserSchema, UserProfileSchema


class UserViewSet(SerializerMixin, PermissionMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'default': UserMeSerializer,
        'me': UserMeSerializer,
        'create_or_update_profile': UserProfileCreateOrUpdateSerializer
    }
    queryset = User.objects.all()

    @UserSchema.me()
    @action(detail=False, methods=['GET'])
    def me(self, request):
        return Response(UserMeSerializer(request.user).data)

    @UserSchema.create_or_update_profile()
    @action(detail=False, methods=['POST'])
    def create_or_update_profile(self, request):
        req_serializer: UserProfileCreateOrUpdateSerializer = self.get_request_serializer()
        user_profile = req_serializer.save()
        res_serializer = UserProfileDisplaySerializer(user_profile)
        return Response(res_serializer.data)


# 无脑 ModelViewSet 的写法
class UserProfileViewSet(SerializerMixin, PermissionMixin, viewsets.ModelViewSet):
    serializer_class = UserProfileModelSerializer

    # serializer_classes = {
    #     'default': UserProfileModelSerializer
    # }
    # queryset = UserProfile.objects.all()
    def get_queryset(self):
        if self.action == 'destroy':
            raise MethodNotAllowed('delete', 'UserProfile 不允许调用 delete 方法')
        if self.action in {'list', 'retrieve'}:
            return UserProfile.objects.all()
        elif self.action in {'pacth', 'put'}:
            return UserProfile.objects.filter(user=self.request.user)
        else:
            return UserProfile.objects.none()

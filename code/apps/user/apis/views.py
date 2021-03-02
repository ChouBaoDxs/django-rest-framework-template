from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from user.apis.serializers import (
    UserMeSerializer,
    UserProfileDisplaySerializer,
    UserProfileCreateOrUpdateSerializer
)
from utils.mixins import SerializerMixin, PermissionMixin
from .schemas import UserSchema


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
        res_serializer = UserProfileDisplaySerializer(user_profile).data
        return Response(res_serializer)

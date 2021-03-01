from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from user.apis.serializers import (
    UserMeSerializer,
    UserProfileSerializer
)
from utils.mixins import SerializerMixin, PermissionMixin
from .schemas import UserSchema


class UserViewSet(SerializerMixin, PermissionMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'default': UserMeSerializer,
        'me': UserMeSerializer,
    }

    @UserSchema.me()
    @action(detail=False, methods=['GET'])
    def me(self, request):
        res_serializer = UserMeSerializer(request.user, context={'request': request})
        return Response(res_serializer.data)

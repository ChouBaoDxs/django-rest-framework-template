from django.db.models import QuerySet
from djangorestframework_camel_case.parser import CamelCaseFormParser, CamelCaseMultiPartParser
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ViewSetMixin, GenericViewSet


class SerializerMixin:
    serializer_classes: dict = None

    def get_serializer_class(self):
        """
        让 ViewSet 支持以下写法（这段代码来自 jumpserver 源码）
        serializer_classes = {
            'default': serializers.AssetUserWriteSerializer,
            'list': serializers.AssetUserReadSerializer,
            'retrieve': serializers.AssetUserReadSerializer,
        }
        """
        serializer_class = None
        if hasattr(self, 'serializer_classes') and isinstance(self.serializer_classes, dict):
            serializer_class = self.serializer_classes.get(self.action, self.serializer_classes.get('default'))
        if serializer_class:
            return serializer_class
        return super().get_serializer_class()

    def get_request_serializer(self, *args, **kwargs):
        """
        校验请求数据并返回请求serializer
        """
        if 'data' not in kwargs:
            kwargs['data'] = self.request.data
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer


class PermissionMixin:
    def get_permissions(self):
        if hasattr(self, 'permission_classes') and isinstance(self.permission_classes, dict):
            default = self.permission_classes.get('default') or api_settings.DEFAULT_PERMISSION_CLASSES
            permission_classes = self.permission_classes.get(self.action, default)
            return [permission() for permission in permission_classes]
        return [permission() for permission in self.permission_classes]


class GenericMixin(SerializerMixin, PermissionMixin):  # 可能还会有其他各种 Mixin
    @property
    def user(self) -> 'User':
        return self.request.user


class FormActionsMixin:
    form_actions = {}

    def get_parsers(self):
        if getattr(self, 'action', None) in self.form_actions:
            # return [FormParser(), MultiPartParser()]
            return [CamelCaseFormParser(), CamelCaseMultiPartParser()]
        return [parser() for parser in self.parser_classes]

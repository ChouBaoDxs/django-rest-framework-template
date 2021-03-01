from rest_framework import serializers
from rest_framework.settings import api_settings


class PermissionMixin:
    def get_permissions(self):
        if hasattr(self, 'permission_classes') and isinstance(self.permission_classes, dict):
            default = self.permission_classes.get('default') or api_settings.DEFAULT_PERMISSION_CLASSES
            permission_classes = self.permission_classes.get(self.action, default)
            return [permission() for permission in permission_classes]
        return [permission() for permission in self.permission_classes]


class SerializerMixin:
    def get_serializer_class(self):
        """
        让 ViewSet 支持以下写法，而不是serializer_class（这段代码来自 jumpserver 源码
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

    def get_request_serializer(self, *args, **kwargs) -> serializers.Serializer:
        """
        校验请求数据并返回请求serializer
        """
        if 'data' not in kwargs:
            kwargs['data'] = self.request.data
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer


class SkipApiLogMixin:
    skip_api_log_actions: set = set()

    def set_request_skip_api_log(self, skip_api_log: bool = True):
        """
        ApiLogMiddleware 会用到
        """
        # self.request 是 drf 的
        # self.request._request 才是 django 的
        setattr(self.request._request, 'skip_api_log', skip_api_log)

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        if self.action in self.skip_api_log_actions:
            self.set_request_skip_api_log(True)

        return response

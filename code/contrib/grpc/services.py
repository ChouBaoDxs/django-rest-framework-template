class SerializerMixin:
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
        if 'message' not in kwargs:
            kwargs['message'] = self.request
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer

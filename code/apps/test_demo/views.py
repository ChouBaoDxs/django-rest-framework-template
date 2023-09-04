from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, serializers, viewsets

from test_demo.models import Category, Product


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


class CategorySer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductListSer(serializers.ModelSerializer):
    category = CategorySer(label='分类')

    class Meta:
        model = Product
        fields = ['id', 'name', 'category']


class ProductViewSet(
    SerializerMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_classes = {
        # 'default': ProductDefaultSer,
        # 'create': ProductCreateSer,
        # 'retrieve': ProductRetrieveSer,
        'list': ProductListSer,
    }
    filterset_fields = ['category']

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.action == 'list':
            queryset = queryset.select_related('category')
        return queryset

    @swagger_auto_schema(operation_summary='产品-列表')
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

from rest_framework import viewsets, mixins, serializers

from goods.models import Goods, GoodsTag


class GoodsTagSer(serializers.ModelSerializer):
    class Meta:
        model = GoodsTag
        fields = ['id', 'name']


class GoodsDisplaySer(serializers.ModelSerializer):
    tags = GoodsTagSer(many=True)

    class Meta:
        model = Goods
        # fields = '__all__' # 一般情况不推荐 __all__
        fields = ['id', 'name', 'tags']


class GoodsCreateOrUpdateSer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ['id', 'name', 'tags']


class GoodsViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_classes = {
        'retrieve': GoodsDisplaySer,
        'list': GoodsDisplaySer,
        'create': GoodsCreateOrUpdateSer,
        'update': GoodsCreateOrUpdateSer,
    }
    queryset = Goods.objects.all()
    permission_classes = []

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_queryset(self):
        queryset = self.queryset
        if self.action in {'retrieve', 'list'}:
            queryset = queryset.prefetch_related('tags')

        return queryset

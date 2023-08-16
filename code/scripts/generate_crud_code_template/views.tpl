from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from {{filter_module_path}} import {{model_name}}Filter
from {{schema_module_path}} import {{model_name}}Schema
from {{serializer_module_path}} import (
    {{model_name}}DefaultSer,
    {{model_name}}RetrieveSer,
    {{model_name}}ListSer,
)
from {{model_module_path}} import {{model_name}}
from contrib.drf.viewset import GenericMixin


class {{model_name}}ViewSet(
    GenericMixin,
    viewsets.ModelViewSet,
):
    serializer_classes = {
        'default': {{model_name}}DefaultSer,
        # 'create': {{model_name}}CreateSer,
        # 'update': {{model_name}}UpdateSer,
        # 'partial_update': {{model_name}}UpdateSer,
        'retrieve': {{model_name}}RetrieveSer,
        'list': {{model_name}}ListSer,
    }
    permission_classes = {
        # 'default': [],
        # 'retrieve': [],
        # 'list': [],
    }
    search_fields = []
    ordering = '-id'
    filterset_class = {{model_name}}Filter

    def get_queryset(self):
        queryset = {{model_name}}.objects.all()
        return queryset

    @{{model_name}}Schema.create()
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @{{model_name}}Schema.update()
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    @{{model_name}}Schema.partial_update()
    def partial_update(self, *args, **kwargs):
        return super().partial_update(*args, **kwargs)

    @{{model_name}}Schema.destroy()
    def destroy(self, *args, **kwargs):
        return super().destroy(*args, **kwargs)

    @{{model_name}}Schema.retrieve()
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @{{model_name}}Schema.list()
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

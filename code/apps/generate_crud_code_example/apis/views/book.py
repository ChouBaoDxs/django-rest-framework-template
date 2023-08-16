from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.generate_crud_code_example.apis.filters.book import BookFilter
from apps.generate_crud_code_example.apis.schemas.book import BookSchema
from apps.generate_crud_code_example.apis.serializers.book import (
    BookDefaultSer,
    BookRetrieveSer,
    BookListSer,
)
from generate_crud_code_example.models import Book
from contrib.drf.viewset import GenericMixin


class BookViewSet(
    GenericMixin,
    viewsets.ModelViewSet,
):
    serializer_classes = {
        'default': BookDefaultSer,
        # 'create': BookCreateSer,
        # 'update': BookUpdateSer,
        # 'partial_update': BookUpdateSer,
        'retrieve': BookRetrieveSer,
        'list': BookListSer,
    }
    permission_classes = {
        # 'default': [],
        # 'retrieve': [],
        # 'list': [],
    }
    search_fields = []
    ordering = '-id'
    filterset_class = BookFilter

    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset

    @BookSchema.create()
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @BookSchema.update()
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    @BookSchema.partial_update()
    def partial_update(self, *args, **kwargs):
        return super().partial_update(*args, **kwargs)

    @BookSchema.destroy()
    def destroy(self, *args, **kwargs):
        return super().destroy(*args, **kwargs)

    @BookSchema.retrieve()
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @BookSchema.list()
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

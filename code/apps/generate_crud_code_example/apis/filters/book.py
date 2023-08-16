from django_filters import rest_framework as filters

from generate_crud_code_example.models import Book


class BookFilter(filters.FilterSet):
    created_at_gte = filters.DateFilter(
        help_text='创建时间下限',
        field_name='created_at',
        lookup_expr='gte',
    )
    created_at_lte = filters.DateFilter(
        help_text='创建时间上限',
        field_name='created_at',
        lookup_expr='lte',
    )
    
    class Meta:
        model = Book
        fields = []

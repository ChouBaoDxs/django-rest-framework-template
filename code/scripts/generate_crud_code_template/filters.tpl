from django_filters import rest_framework as filters

from {{model_module_path}} import {{model_name}}


class {{model_name}}Filter(filters.FilterSet):
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
    {{special_filter_field_code}}
    class Meta:
        model = {{model_name}}
        fields = []

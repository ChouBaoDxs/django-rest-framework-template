from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import QuerySet
from rest_framework.compat import coreapi, coreschema
from rest_framework.request import Request
from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend

from utils.date_and_time import str2datetime

DEFAULT_FILTER_BACKENDS = [DjangoFilterBackend, SearchFilter, OrderingFilter]


class CreatedAtFilter(BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        created_at__gte = request.query_params.get('created_at_gte')
        created_at__lte = request.query_params.get('created_at_lte')
        if created_at__gte:
            created_at__gte = str2datetime(created_at__gte)
        if created_at__lte:
            created_at__lte = str2datetime(created_at__lte)
        try:
            if created_at__gte:
                queryset = queryset.filter(created_at__gte=created_at__gte)
            if created_at__lte:
                queryset = queryset.filter(created_at__lte=created_at__lte)
            return queryset
        except:
            return queryset

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='created_at_gte',
                required=False,
                location='query',
                schema=coreschema.String(
                    title='created_at_gte',
                    description='创建时间查询-起始'
                )
            ),
            coreapi.Field(
                name='created_at_lte',
                required=False,
                location='query',
                schema=coreschema.String(
                    title='created_at_lte',
                    description='创建时间查询-终止'
                )
            )
        ]

    # def get_schema_operation_parameters(self, view):
    #     return [
    #         {
    #             'name': 'created_at_gte',
    #             'required': False,
    #             'in': 'query',
    #             'description': '创建时间查询-起始',
    #             'schema': {
    #                 'type': 'string',
    #             },
    #         },
    #         {
    #             'name': 'created_at_lte',
    #             'required': False,
    #             'in': 'query',
    #             'description': '创建时间查询-终止',
    #             'schema': {
    #                 'type': 'string',
    #             },
    #         },
    #     ]


CREATED_AT_FILTER_BACKENDS = DEFAULT_FILTER_BACKENDS + [CreatedAtFilter]

from datetime import datetime, timedelta

from django.db.models import QuerySet
from django.http.request import HttpRequest
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers

from utils.validators import (
    validate_phone,
)
from utils.date_and_time import str2datetime
from utils.paginations import DefaultPageNumberPagination


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, help_text='手机号', validators=[validate_phone])

class ExcelSerializer(serializers.Serializer):
    excel = serializers.FileField(required=True, help_text='excel文件')

class CreatedAtSerializer(serializers.Serializer):
    created_at_gte = serializers.CharField(required=False)
    created_at_lte = serializers.CharField(required=False)

    def validate_created_at_gte(self, created_at_gte):
        created_at_gte = str2datetime(created_at_gte)
        if created_at_gte:
            return created_at_gte
        else:
            raise serializers.ValidationError('非法的created_at_gte')

    def validate_created_at_lte(self, created_at_lte):
        created_at_lte = str2datetime(created_at_lte)
        if created_at_lte:
            return created_at_lte
        else:
            raise serializers.ValidationError('非法的created_at_lte')


class DateSerializer(serializers.Serializer):
    date_gte = serializers.CharField(required=False)
    date_lte = serializers.CharField(required=False)

    def validate_date_gte(self, date_gte):
        date_gte = str2datetime(date_gte).date()
        if date_gte:
            return date_gte
        else:
            raise serializers.ValidationError('非法的date_gte')

    def validate_date_lte(self, date_lte):
        date_lte = str2datetime(date_lte).date()
        if date_lte:
            return date_lte
        else:
            raise serializers.ValidationError('非法的date_lte')

    class Meta:  # 这个是给 QuerySerializer 用的
        simple_filter_fields = [
            {'field': 'date', 'lookup_expr': 'gte'},
            {'field': 'date', 'lookup_expr': 'lte'},
        ]

    def set_default_date_value(self, attrs: dict) -> dict:
        now_date = datetime.now().date()
        if 'date_gte' not in attrs:
            attrs['date_gte'] = now_date - timedelta(days=7)
        if 'date_lte' not in attrs:
            attrs['date_lte'] = now_date
        return attrs


class PageNumberPaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=20)
    pagination_class = DefaultPageNumberPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None

        if not hasattr(self, '_validated_data'):
            self.is_valid(True)
        v_data: dict = self.validated_data

        request: Request = Request(HttpRequest())
        request.query_params.setlist('page', [v_data['page']])
        request.query_params.setlist('page_size', [v_data['page_size']])
        return self.paginator.paginate_queryset(queryset, request)

    def generate_paginate_response(self, queryset: QuerySet, response_serializer) -> Response:
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = response_serializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        serializer = response_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderingSerializer(serializers.Serializer):
    ordering = serializers.CharField(required=False, help_text='排序，多个条件排序就以英文逗号隔开')

    def validate_ordering(self, value: str) -> list:
        return [_.strip() for _ in value.split(',')]

    def filter_queryset_by_ordering(self, queryset):
        v_data: dict = self.validated_data
        ordering: list = v_data.get('ordering')

        if ordering:
            return queryset.order_by(*ordering)

        return queryset


class QuerySerializer(OrderingSerializer):
    class Meta:
        # 下面是定义查询参数的例子，继承了 QuerySerializer 之后必须要
        simple_filter_fields = [
            # {'field': 'stock_num', 'lookup_expr': 'gte'},
            # {'field': 'stock_num', 'lookup_expr': 'lte'},
            # {'field': 'created_at', 'lookup_expr': 'gte'},
            # {'field': 'created_at', 'lookup_expr': 'lte'},
            # {'field': 'user_id', 'lookup_expr': 'exact'},
        ]

    def perform_filter_queryset(self, queryset: QuerySet) -> QuerySet:
        """
        可以重写这个方法来嵌入自己的查询逻辑
        """
        return queryset

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if not hasattr(self, '_validated_data'):
            self.is_valid(True)
        v_data: dict = self.validated_data

        queryset = self.perform_filter_queryset(queryset)  # 自定义过滤方法
        queryset = self.filter_queryset_by_ordering(queryset)  # 排序

        # 收集所有 simple_filter_fields，比如自己写的查询 Serializer 继承了 DateSerializer 和
        # QuerySerializer，下面这段代码就可以收集到 DateSerializer 的 Meta
        simple_filter_fields = []
        for e in self.__class__.mro():
            s = super(e, self)
            meta_class = getattr(s, 'Meta', None)
            if meta_class:
                meta_simple_filter_fields = getattr(meta_class, 'simple_filter_fields', None)
                if isinstance(meta_simple_filter_fields, list):
                    simple_filter_fields.extend(meta_simple_filter_fields)

        simple_filter_fields = self.Meta.simple_filter_fields
        for filter_field in simple_filter_fields:
            field = filter_field['field']
            lookup_expr = filter_field['lookup_expr']
            if lookup_expr == 'exact':
                if field not in v_data:
                    continue
                value = v_data[field]
                field_name = filter_field.get('field_name') or field
                lookup = f'{field_name}__{lookup_expr}'
                queryset = queryset.filter(**{lookup: value})
            else:
                value = v_data.get(f'{field}_{lookup_expr}')
                if value is not None:
                    field_name = filter_field.get('field_name') or field
                    lookup = f'{field_name}__{lookup_expr}'
                    queryset = queryset.filter(**{lookup: value})
        return queryset

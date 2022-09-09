from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, unset
from rest_framework import serializers
from rest_framework.compat import coreapi, coreschema


class BaseSchema:
    TAGS = []

    @classmethod
    def schema(cls,  # 写 swagger_auto_schema_wrapper 太长了，弄个短的
               method=None, methods=None, auto_schema=unset, request_body=None, query_serializer=None,
               manual_parameters=None, operation_id=None, operation_description=None, operation_summary=None,
               security=None, deprecated=None, responses=None, field_inspectors=None, filter_inspectors=None,
               paginator_inspectors=None, tags=None, **extra_overrides):
        if not tags:
            tags = cls.TAGS
        return swagger_auto_schema(
            method=method, methods=methods, auto_schema=auto_schema, request_body=request_body, query_serializer=query_serializer,
            manual_parameters=manual_parameters, operation_id=operation_id, operation_description=operation_description, operation_summary=operation_summary,
            security=security, deprecated=deprecated, responses=responses, field_inspectors=field_inspectors, filter_inspectors=filter_inspectors,
            paginator_inspectors=paginator_inspectors, tags=tags, **extra_overrides
        )


def serializer_to_schema_fields(serializer_class) -> list:
    """
    根据 Serializer 生成 schema_fields，常用于继承 BaseFilterBackend 的 get_schema_fields 方法
    """
    ser = serializer_class()
    schema_fields = []
    for field_name, field in ser.fields.items():
        schema_class = coreschema.Integer if isinstance(field, serializers.IntegerField) else coreschema.String
        schema_fields.append(coreapi.Field(
            name=field_name,
            required=field.required,
            location='query',
            schema=schema_class(
                title=field_name,
                description=field.help_text,
            )
        ))
    return schema_fields


def serializer_to_manual_parameters(serializer_class, in_=openapi.IN_QUERY) -> list:
    """
    根据 Serializer 生成 drf_yasg 的 manual_parameters
    """
    ser = serializer_class()
    manual_parameters = []
    for field_name, field in ser.fields.items():
        if isinstance(field, serializers.IntegerField):
            type_ = openapi.TYPE_INTEGER
        elif isinstance(field, serializers.FileField):
            type_ = openapi.TYPE_FILE
        else:
            type_ = openapi.TYPE_STRING
        manual_parameters.append(openapi.Parameter(
            field_name,
            in_,
            description=field.help_text,
            required=field.required,
            type=type_
        ))
    return manual_parameters

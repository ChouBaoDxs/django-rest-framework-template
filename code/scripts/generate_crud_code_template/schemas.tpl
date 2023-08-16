from drf_yasg import openapi

from contrib.drf.schema import BaseSchema


class {{model_name}}Schema(BaseSchema):
    TAGS = ['{{model_verbose_name}}']

    @classmethod
    def create(cls):
        return cls.schema(operation_summary='{{model_verbose_name}}-创建')

    @classmethod
    def update(cls):
        return cls.schema(operation_summary='{{model_verbose_name}}-更新')

    @classmethod
    def partial_update(cls):
        return cls.schema(operation_summary='{{model_verbose_name}}-更新')

    @classmethod
    def destroy(cls):
        return cls.schema(operation_summary='{{model_verbose_name}}-删除')

    @classmethod
    def retrieve(cls):
        return cls.schema(operation_summary='{{model_verbose_name}}-详情')

    @classmethod
    def list(cls):
        return cls.schema(operation_summary='{{model_verbose_name}}-列表')

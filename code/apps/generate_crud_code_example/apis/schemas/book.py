from drf_yasg import openapi

from contrib.drf.schema import BaseSchema


class BookSchema(BaseSchema):
    TAGS = ['书籍']

    @classmethod
    def create(cls):
        return cls.schema(operation_summary='书籍-创建')

    @classmethod
    def update(cls):
        return cls.schema(operation_summary='书籍-更新')

    @classmethod
    def partial_update(cls):
        return cls.schema(operation_summary='书籍-更新')

    @classmethod
    def destroy(cls):
        return cls.schema(operation_summary='书籍-删除')

    @classmethod
    def retrieve(cls):
        return cls.schema(operation_summary='书籍-详情')

    @classmethod
    def list(cls):
        return cls.schema(operation_summary='书籍-列表')

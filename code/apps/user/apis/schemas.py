from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.schemas import ManualSchema

from contrib.drf.schema import BaseSchema

from .serializers import (
    UserMeSerializer,
    UserProfileDisplaySerializer,
)


class UserSchema(BaseSchema):
    TAGS = ['用户/用户']

    @classmethod
    def fake_error(cls):
        return cls.schema(
            operation_id='user-模拟错误响应',
        )

    @classmethod
    def fake_success(cls):
        return cls.schema(
            operation_id='user-模拟成功响应',
            manual_parameters=[
                openapi.Parameter(
                    'traceparent',
                    openapi.IN_HEADER,
                    default='00-138286cb34e04a0811a8aa6965ea410f-93c98b42962922e1-01',
                    required=False,
                    type=openapi.TYPE_STRING,
                ),
            ],
        )

    @classmethod
    def me(cls):
        return cls.schema(
            operation_id='user-获取当前用户信息',
            operation_description='获取当前用户信息',
            responses={'200': UserMeSerializer()},
        )

    @classmethod
    def create_or_update_profile(cls):
        return cls.schema(
            operation_id='user-创建或修改当前用户个人信息',
            operation_description='创建或修改当前用户个人信息',
            responses={'200': UserProfileDisplaySerializer()},
        )


class UserProfileSchema:
    pass

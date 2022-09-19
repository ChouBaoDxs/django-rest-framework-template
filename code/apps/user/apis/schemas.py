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

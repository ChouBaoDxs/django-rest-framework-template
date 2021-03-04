from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.schemas import ManualSchema

from .serializers import (
    UserMeSerializer,
    UserProfileDisplaySerializer,
)


class UserSchema:
    @staticmethod
    def me():
        return swagger_auto_schema(
            operation_id='user-获取当前用户信息',
            operation_description='获取当前用户信息',
            responses={'200': UserMeSerializer()},
        )

    @staticmethod
    def create_or_update_profile():
        return swagger_auto_schema(
            operation_id='user-创建或修改当前用户个人信息',
            operation_description='创建或修改当前用户个人信息',
            responses={'200': UserProfileDisplaySerializer()},
        )


class UserProfileSchema:
    pass

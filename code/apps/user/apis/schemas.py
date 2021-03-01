from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.schemas import ManualSchema

from .serializers import (
    UserMeSerializer,
    UserProfileSerializer
)


class UserSchema:
    @staticmethod
    def me():
        return swagger_auto_schema(
            operation_id='user-获取当前用户信息',
            operation_description='获取当前用户信息',
            responses={'200': UserMeSerializer()},
        )

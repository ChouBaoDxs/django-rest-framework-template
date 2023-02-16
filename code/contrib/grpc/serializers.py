from django.conf import settings
from django_socio_grpc import proto_serializers
from django_socio_grpc.exceptions import InvalidArgument
from rest_framework.exceptions import ValidationError


class IsValidMixin:
    if settings.IS_GRPC_SERVER:
        def is_valid(self, raise_exception=False):
            try:
                return super().is_valid(raise_exception=raise_exception)
            except ValidationError as e:
                raise InvalidArgument(self._errors)


class ModelProtoSerializer(IsValidMixin, proto_serializers.ModelProtoSerializer):
    pass

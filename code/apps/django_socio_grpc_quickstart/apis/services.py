from django_socio_grpc import generics
from django_socio_grpc.decorators import grpc_action

from django_socio_grpc_quickstart.models import Question
from django_socio_grpc_quickstart.apis.serializers import (
    QuestionProtoSerializer,
    QuestionCustomRetrieveProtoSerializer,
    QuestionBaseProtoExampleSerializer,
    MethodSerializerFieldExampleSerializer,
)


class QuestionService(generics.AsyncModelService):
    queryset = Question.objects.all()
    serializer_class = QuestionProtoSerializer

    @grpc_action(
        request=[{"name": "id", "type": "int32"}],
        response=QuestionCustomRetrieveProtoSerializer,
    )
    async def CustomRetrieve(self, request, context):
        instance = self.get_object()
        serializer = QuestionCustomRetrieveProtoSerializer(instance)
        return serializer.message

    @grpc_action(
        request=[{"name": "id", "type": "int32"}],
        response=QuestionBaseProtoExampleSerializer,
    )
    async def CustomRetrieveWithBaseProtoSerializer(self, request, context):
        instance = self.get_object()
        serializer = QuestionBaseProtoExampleSerializer(instance)
        return serializer.message

    @grpc_action(
        request='google.protobuf.Empty',
        response=MethodSerializerFieldExampleSerializer,
    )
    async def MethodSerializerFieldExample(self, request, context):
        serializer = MethodSerializerFieldExampleSerializer(data={})
        serializer.is_valid()
        return serializer.message

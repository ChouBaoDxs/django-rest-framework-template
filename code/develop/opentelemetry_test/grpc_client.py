import json

import grpc
from google.protobuf.json_format import MessageToDict

import django_socio_grpc_quickstart.grpc.django_socio_grpc_quickstart_pb2 as quickstart_pb2
from django_socio_grpc_quickstart.grpc.django_socio_grpc_quickstart_pb2_grpc import QuestionControllerStub
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from utils import init_jaeger_tracer

init_jaeger_tracer(service_name='grpc-client')
GrpcInstrumentorClient().instrument()


class QuestionServiceCaller:
    channel = grpc.insecure_channel('127.0.0.1:50051')
    client = QuestionControllerStub(channel)

    @classmethod
    def List(cls):
        request = quickstart_pb2.QuestionListRequest()
        return cls.client.List(request)


if __name__ == '__main__':
    rsp = QuestionServiceCaller.List()
    dict_result = MessageToDict(
        rsp,
        preserving_proto_field_name=True,
        use_integers_for_enums=True,
        including_default_value_fields=True,
    )
    print(json.dumps(dict_result, ensure_ascii=False, indent=2))

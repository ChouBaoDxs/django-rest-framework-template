import json

import grpc
from google.protobuf.json_format import MessageToDict

import django_socio_grpc_quickstart.grpc.django_socio_grpc_quickstart_pb2 as quickstart_pb2
from django_socio_grpc_quickstart.grpc.django_socio_grpc_quickstart_pb2_grpc import QuestionControllerStub


class QuestionServiceCaller:
    channel = grpc.insecure_channel('127.0.0.1:50051')
    client = QuestionControllerStub(channel)

    @classmethod
    def Create(cls):
        request = quickstart_pb2.QuestionRequest(
            # question_text='question 4',
            # pub_date='2022-01-10 13:00:00'
            # pub_date=''
        )
        return cls.client.Create(request)

    @classmethod
    def Retrieve(cls):
        request = quickstart_pb2.QuestionRetrieveRequest(id=1)
        return cls.client.Retrieve(request)

    @classmethod
    def List(cls):
        request = quickstart_pb2.QuestionListRequest()
        return cls.client.List(request)

    @classmethod
    def CustomRetrieve(cls):
        request = quickstart_pb2.QuestionCustomRetrieveRequest(id=1)
        return cls.client.CustomRetrieve(request)

    @classmethod
    def CustomRetrieveWithBaseProtoSerializer(cls):
        request = quickstart_pb2.QuestionCustomRetrieveWithBaseProtoSerializerRequest(id=4)
        return cls.client.CustomRetrieveWithBaseProtoSerializer(request)
    
    @classmethod
    def MethodSerializerFieldExample(cls):
        request = quickstart_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return cls.client.MethodSerializerFieldExample(request)

if __name__ == '__main__':
    # rsp = QuestionServiceCaller.Create()
    rsp = QuestionServiceCaller.Retrieve()
    # rsp = QuestionServiceCaller.List()
    # rsp = QuestionServiceCaller.CustomRetrieve()
    # rsp = QuestionServiceCaller.CustomRetrieveWithBaseProtoSerializer()
    # rsp = QuestionServiceCaller.MethodSerializerFieldExample()
    dict_result = MessageToDict(
        rsp,
        preserving_proto_field_name=True,
        use_integers_for_enums=True,
        including_default_value_fields=True,
    )
    print(json.dumps(dict_result, ensure_ascii=False, indent=2))

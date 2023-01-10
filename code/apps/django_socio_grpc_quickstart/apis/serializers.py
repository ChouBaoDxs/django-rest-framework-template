import typing

from django_socio_grpc import proto_serializers
from rest_framework import serializers
from rest_framework.fields import DateTimeField

from django_socio_grpc_quickstart.models import Question
import django_socio_grpc_quickstart.grpc.django_socio_grpc_quickstart_pb2 as quickstart_pb2


class NullableDatetimeField(DateTimeField):  # 由于 grpc 总是具有默认值，这里处理当日期类型入参为空字符串时，转为 None
    def to_internal_value(self, value):
        if not value:
            return None
        return super().to_internal_value(value)


class QuestionProtoSerializer(proto_serializers.ModelProtoSerializer):
    pub_date = NullableDatetimeField(validators=[])

    class Meta:
        model = Question
        proto_class = quickstart_pb2.QuestionResponse
        proto_class_list = quickstart_pb2.QuestionListResponse
        # message_list_attr = 'list_custom_field_name' # 列表接口的结果字段默认是 results，可以自定义
        fields = ['id', 'question_text', 'pub_date']


class QuestionCustomRetrieveProtoSerializer(proto_serializers.ModelProtoSerializer):
    pub_date = NullableDatetimeField(validators=[])
    dict_data = serializers.DictField(required=False)

    class Meta:
        model = Question
        proto_class = quickstart_pb2.QuestionCustomRetrieveResponse
        fields = ['id', 'question_text', 'pub_date', 'dict_data']

    def to_representation(self, instance: Question):
        ret = super().to_representation(instance)
        ret['dict_data'] = {'key': 'value'}
        return ret


class QuestionBaseProtoExampleSerializer(proto_serializers.BaseProtoSerializer):  # BaseProtoSerializer 需要自己声明字段类型
    class Meta:
        pass
        proto_class = quickstart_pb2.QuestionBaseProtoExampleResponse

    def to_representation(self, instance: Question):
        return {
            'id': instance.id,
            'question_text': instance.question_text,
            'pub_date': str(instance.pub_date) if instance.pub_date else '',
        }

    def to_proto_message(self):
        return [
            {'name': 'id', 'type': 'int32'},
            {'name': 'question_text', 'type': 'string'},
            {'name': 'pub_date', 'type': 'string'},
        ]


class MethodSerializerFieldExampleSerializer(proto_serializers.ProtoSerializer):
    default_method_field = serializers.SerializerMethodField()
    custom_method_field = serializers.SerializerMethodField(method_name='custom_method')

    def get_default_method_field(self, obj) -> int:
        return 3

    def custom_method(self, obj) -> typing.List[typing.Dict]:
        return [{'test': 'test'}]

    class Meta:
        proto_class = quickstart_pb2.MethodSerializerFieldExampleResponse
        fields = ['default_method_field', 'custom_method_field']

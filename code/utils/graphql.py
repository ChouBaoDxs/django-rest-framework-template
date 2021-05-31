import graphene
from graphene_django.utils import camelize
from graphql.language.ast import BooleanValue, StringValue, IntValue, ListValue, ObjectValue, FloatValue
from rest_framework.utils import encoders, json


class JsonField(graphene.Scalar):
    """
    代码来自 http://wxnacy.com/2018/02/14/graphene-type-json/
    """

    @staticmethod
    def identity(value):
        if isinstance(value, (str, bool, int, float)):
            return value.__class__(value)
        elif isinstance(value, (list, dict)):
            return value
        else:
            return None

    serialize = identity
    parse_value = identity

    @staticmethod
    def parse_literal(ast):
        if isinstance(ast, (StringValue, BooleanValue)):
            return ast.value
        elif isinstance(ast, IntValue):
            return int(ast.value)
        elif isinstance(ast, FloatValue):
            return float(ast.value)
        elif isinstance(ast, ListValue):
            return [JsonField.parse_literal(value) for value in ast.values]
        elif isinstance(ast, ObjectValue):
            return {field.name.value: JsonField.parse_literal(field.value) for field in ast.fields}
        else:
            return None


class OutputJsonField(graphene.JSONString):
    @staticmethod
    def serialize(dt):
        return dt


class OutputCamelizeJsonField(graphene.JSONString):
    @staticmethod
    def serialize(dt):
        return camelize(dt)


class OutputDrfCamelizeJsonField(graphene.JSONString):
    @staticmethod
    def serialize(dt):
        dt = camelize(dt)
        json_dump = json.dumps(dt, cls=encoders.JSONEncoder)
        return json.loads(json_dump)

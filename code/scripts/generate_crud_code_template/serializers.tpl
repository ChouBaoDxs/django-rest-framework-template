from rest_framework import serializers

from {{model_module_path}} import {{model_name}}


class {{model_name}}DefaultSer(serializers.ModelSerializer):
    {{default_ser_special_field_code | safe}}
    class Meta:
        model = {{model_name}}
        fields = {{default_ser_fields | safe}}

    {{default_ser_create_method_code | safe}}
class {{model_name}}RetrieveSer(serializers.ModelSerializer):
    class Meta:
        model = {{model_name}}
        fields = {{retrieve_ser_fields | safe}}


class {{model_name}}ListSer(serializers.ModelSerializer):
    class Meta:
        model = {{model_name}}
        fields = {{list_ser_fields | safe}}

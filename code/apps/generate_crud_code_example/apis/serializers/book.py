from rest_framework import serializers

from generate_crud_code_example.models import Book


class BookDefaultSer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['id', 'name', 'desc', 'kind']

    def create(self, validated_data):
        validated_data['creator_id'] = self.context['request'].user.id
        return super().create(validated_data)


class BookRetrieveSer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'created_at', 'updated_at', 'creator_id', 'name', 'desc', 'kind']


class BookListSer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'created_at', 'updated_at', 'creator_id', 'name', 'kind']

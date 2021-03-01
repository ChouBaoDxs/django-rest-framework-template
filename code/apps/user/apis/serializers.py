from django.contrib.auth.models import User, Group
from rest_framework import serializers

from user.models import (
    UserProfile,
)


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

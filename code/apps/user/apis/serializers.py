from django.contrib.auth.models import User, Group
from rest_framework import serializers

from user.models import (
    UserProfile,
)
from utils.validators import validate_phone


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'phone', 'desc']


class UserProfileCreateOrUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(help_text='手机号', validators=[validate_phone])
    desc = serializers.CharField(help_text='个人介绍', max_length=255)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserProfile
        fields = ['phone', 'desc', 'user']

    def save(self, **kwargs):
        # user: User = self.context['request'].user
        validated_data = self.validated_data
        defaults = {
            'phone': validated_data['phone'],
            'desc': validated_data['desc'],
        }
        filter_kwargs = {
            'user': validated_data['user']
        }
        user_profile, created = UserProfile.objects.update_or_create(defaults=defaults, **filter_kwargs)
        return user_profile

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


class UserProfileModelSerializer(serializers.ModelSerializer):
    # 指定两个可修改字段的校验逻辑，不严格校验的话可以省略
    phone = serializers.CharField(help_text='手机号', validators=[validate_phone])
    desc = serializers.CharField(help_text='个人介绍', max_length=255)

    class Meta:
        model = UserProfile
        # fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def save(self, **kwargs):
        user = self.context['request'].user
        if self.instance is None:
            # 说明想新建，校验是否已经存在该用户对应的 profile
            if UserProfile.objects.filter(user=user).first():
                raise serializers.ValidationError('不允许重复创建 profile !')
        kwargs['user'] = user
        return super().save(**kwargs)


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

import uuid, requests
from rest_framework import serializers
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email",)


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password,])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'telegram_chat_id', 'password', 'password_confirm', 'is_staff',)
        read_only_field = ('is_staff', 'telegram_chat_id')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            return serializers.ValidationError({"password": "Passwords fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            telegram_chat_id='telegram_chat_id',
        )
        user.set_password(validated_data['password'])
        user.save()

        return user




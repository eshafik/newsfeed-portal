from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password as v_passwords

from apps.user.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'name', 'email')
        extra_kwargs = {'username': {'read_only': True}}

    def validate_password(self, value: str) -> str:
        try:
            v_passwords(value, User)
            return make_password(value)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(e.messages)

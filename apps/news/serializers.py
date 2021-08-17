from rest_framework import serializers

from apps.user.models import UserPreference


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        exclude = ('user', )

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from djoser.serializers import UserCreateSerializer

from .models import User


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Собственный сериализатор для функции регистрации.
    """
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'password')


class LogoutSerializer(serializers.Serializer):
    """
    Сериализатор для функции выхода из учётной записи.
    """
    refresh = serializers.CharField()

    def validate(self, attrs):
        try:
            self.token = RefreshToken(attrs["refresh"])
        except TokenError:
            raise serializers.ValidationError("Invalid or expired token.")
        return attrs

    def save(self, **kwargs):
        try:
            self.token.blacklist()
        except TokenError:
            raise serializers.ValidationError("Token already blacklisted or invalid.")

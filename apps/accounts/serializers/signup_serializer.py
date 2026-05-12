import re

from django_redis import cache
from rest_framework import serializers

from apps.accounts.models.signup_models import Account


class SignUpRequestSerializer(serializers.ModelSerializer):
    email_token = serializers.CharField(write_only=True)
    password = serializers.CharField(
        write_only=True,
    )
    password_confirm = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = Account
        fields = [
            "nickname",
            "email_token",
            "password",
            "password_confirm",
        ]
        extra_kwargs = {
            "nickname": {"validators": []},
        }

    def validate_email_token(self, value: str) -> str:
        cache_key = f"email_token_{value}"
        cache_data = cache.get(cache_key)
        if not cache_data:
            raise serializers.ValidationError("This email is not registered")
        return value

    def validate_password(self, data: str) -> str:
        """Password must be 8-15 chars, include letter, number, and special character."""
        if not 8 <= len(data) <= 15:
            raise serializers.ValidationError("Password must be between 8 and 15 characters")
        if not re.search(r"[a-zA-Z]", data):
            raise serializers.ValidationError("Password must contain at least one letter")
        if not re.search(r"\d", data):
            raise serializers.ValidationError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", data):
            raise serializers.ValidationError("Password must contain at least one special character")
        return data

    def validate(self, data: dict) -> dict:
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Passwords must match")
        return data


class AccountResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            "email",
            "nickname",
        ]

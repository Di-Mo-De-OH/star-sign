import re

from rest_framework import serializers

from apps.accounts.models import Account


class EmailSendSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailVerifySerializer(serializers.Serializer):
    token = serializers.CharField()
    code = serializers.CharField()


class SignUpRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    email_token = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = [
            "email",
            "password",
            "password_confirm",
            "nickname",
            "email_token",
        ]

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
            raise serializers.ValidationError("Passwords don't match")
        return data

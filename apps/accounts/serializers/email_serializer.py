
from rest_framework import serializers


class EmailSendSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.RegexField(
        regex=r"^[a-zA-Z0-9]{6}$",
        required=True
    )

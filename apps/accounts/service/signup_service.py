from typing import Any

from django.db import transaction
from django.db.models import Q
from django_redis import cache
from rest_framework.exceptions import ValidationError

from apps.accounts.models.signup_models import Account


class SignUpService:
    def create_user(self, validated_data: Any) -> Account:

        email_token = validated_data.pop("email_token")
        password = validated_data.pop("password")
        validated_data.pop("password_confirm")
        nickname = validated_data.pop("nickname")

        email_key = f"email_token_{email_token}"
        email_data = cache.get(email_key)

        if not email_data:
            raise ValidationError("Email is not valid.")

        email = email_data.get("email")

        if not email:
            raise ValidationError("Email is not valid.")

        with transaction.atomic():
            existing_accounts = Account.objects.select_for_update().filter(Q(email=email) | Q(nickname=nickname))
            for account in existing_accounts:
                if account.email == email:
                    raise ValidationError("Email is already registered.")
                if account.nickname == nickname:
                    raise ValidationError("Nickname is already registered.")

            account = Account.objects.create_user(email=email, nickname=nickname, password=password, **validated_data)
            account.is_active = True
            account.save()
            cache.delete(email_key)
            return account

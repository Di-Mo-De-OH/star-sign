from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.core.models import TimeStampedModel


class AccountManager(BaseUserManager["Account"]):
    def create_user(self, email: str, password: str | None = None, **extra_fields: Any) -> "Account":
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields: Any) -> "Account":
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email = models.EmailField(max_length=255, unique=True, null=False)
    nickname = models.CharField(max_length=50, unique=True, null=False)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self) -> str:
        return self.email


# class SocialAccount(TimeStampedModel):
#     class Provider(models.TextChoices):
#         KAKAO = "kakao", "Kakao"
#
#     user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="social_accounts")
#     provider = models.CharField(max_length=10, choices=Provider.choices)
#     provider_id = models.CharField(max_length=255)
#
#     class Meta:
#         unique_together = ("provider", "provider_id")

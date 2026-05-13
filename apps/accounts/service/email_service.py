import secrets
import uuid

from django.core.mail import send_mail
from django_redis import cache
from redis import RedisError
from rest_framework.exceptions import ValidationError

from apps.core.exceptions import ExpiredException
from apps.core.utils import Base62


class EmailSendService:

    def send_email(self, email: str) -> None:
        code = Base62.uuid_encode(uuid.uuid4(), length=6)
        cache_key = f"email_{email}"
        try:
            cache.set(cache_key, code, timeout=180)
        except RedisError:
            raise ValidationError("Server error. Please try again.")

        try:
            send_mail(
                subject="[Stat-Sign] verification code",
                from_email="",
                message=f"Verification code: {code}",
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception:
            cache.delete(cache_key)
            raise ValidationError("Failed to send email.")

    def verify_code(self, email: str, code: str) -> str:
        cache_key = f"email_{email}"
        try:
            cache_data = cache.get(cache_key)
        except RedisError:
            raise ValidationError("Server error. Please try again.")

        if not cache_data:
            raise ExpiredException()
        if cache_data != code:
            raise ExpiredException("Your code is false")

        verify_token = secrets.token_urlsafe(32)

        token_key = f"email_token_{verify_token}"
        data = {"email": email, "code": code}
        try:
            cache.set(token_key, data, timeout=600)
        except RedisError:
            raise ValidationError("Server error. Please try again.")
        cache.delete(cache_key)
        return verify_token

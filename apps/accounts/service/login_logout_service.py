from datetime import datetime

from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken


class LoginService:

    def login(self, email: str, password: str, old_refresh_token: str):
        account = authenticate(email=email, password=password)
        if not account:
            raise ValidationError("Email or Password is required")
        if old_refresh_token:
            token = RefreshToken(old_refresh_token)  # type: ignore
            jti = token["jti"]

            cache_key = f"blacklist_refresh_{jti}"
            if cache.get(cache_key):
                raise ValidationError("Blacklist refresh token")

            expire_at = token["exp"]  # unix timestamp
            now = int(datetime.now().timestamp())  # type: ignore
            ttl = expire_at - now

            cache.set(cache_key, "1", timeout=ttl)

        refresh = RefreshToken.for_user(account)
        access_token, refresh_token = str(refresh.access_token), str(refresh)

        return access_token, refresh_token


class LogoutService:
    def logout(self, refresh_token: str) -> None:

        token = RefreshToken(refresh_token)  # type: ignore
        jti = token["jti"]
        cache_key = f"blacklist_refresh_{jti}"

        expire_at = token["exp"]  # unix timestamp
        now = int(datetime.now().timestamp())  # type: ignore
        ttl = expire_at - now
        cache.set(cache_key, "1", timeout=ttl)

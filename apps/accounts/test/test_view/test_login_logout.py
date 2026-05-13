from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import Account


class BaseViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.account = Account.objects.create_user(
            email="test@test.com", password="Test@1234", nickname="test", is_active=True
        )


class LoginViewTest(BaseViewTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_success(self):
        url = reverse("accounts:login")
        response = self.client.post(url, {"email": "test@test.com", "password": "Test@1234"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_credentials_error(self) -> None:
        url = reverse("accounts:login")
        response = self.client.post(url, {"email": "test2@test.com", "password": "Test@1234"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_relogin_token_rotation_success(self) -> None:
        url = reverse("accounts:login")
        response = self.client.post(url, {"email": "test@test.com", "password": "Test@1234"})
        first_refresh_token = response.cookies["refresh_token"].value
        self.client.cookies["refresh_token"] = first_refresh_token
        response_second = self.client.post(url, {"email": "test@test.com", "password": "Test@1234"})
        second_refresh_token = response_second.cookies["refresh_token"].value
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_second.status_code, status.HTTP_200_OK)
        self.assertNotEqual(first_refresh_token, second_refresh_token)

    def test_login_blacklisted_token_error(self) -> None:
        url = reverse("accounts:login")
        response = self.client.post(url, {"email": "test@test.com", "password": "Test@1234"})
        refresh_token = response.cookies["refresh_token"].value
        token = RefreshToken(refresh_token)
        jti = token["jti"]
        cache.set(f"blacklist_refresh_{jti}", "1", timeout=600)
        self.client.cookies["refresh_token"] = refresh_token
        response_second = self.client.post(url, {"email": "test@test.com", "password": "Test@1234"})
        self.assertEqual(response_second.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutViewTest(BaseViewTest):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    def setUp(self) -> None:
        self.client = APIClient()
        login_response = self.client.post(
            reverse("accounts:login"), {"email": "test@test.com", "password": "Test@1234"}
        )
        self.access_token = login_response.data["access_token"]
        self.refresh_token = login_response.cookies["refresh_token"].value

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.client.cookies["refresh_token"] = self.refresh_token

        url = reverse("accounts:logout")
        response = self.client.post(
            url,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.cookies["refresh_token"].value, "")

    def test_logout_no_cookie_error(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.client.cookies.clear()
        url = reverse("accounts:logout")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Account


class BaseViewTest(APITestCase):
    account: Account

    @classmethod
    def setUpTestData(cls) -> None:
        cls.account = Account.objects.create_user(
            email="test@test.com",
            password="Testpassword1",
            nickname="test",
        )


class SignUpViewTest(BaseViewTest):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    @patch("apps.accounts.serializers.signup_serializer.cache")
    @patch("apps.accounts.service.signup_service.cache")
    def test_signup_success(self, mock_cache, mock_serializer_cache) -> None:
        mock_cache.get.return_value = {"email": "test2@test.com"}
        mock_serializer_cache.get.return_value = {"email": "test2@test.com"}

        response = self.client.post(
            reverse("accounts:signup"),
            {
                "email_token": "valid-token",
                "nickname": "newuser",
                "password": "Test@1234",
                "password_confirm": "Test@1234",
            },
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["account"]["nickname"], "newuser")

    @patch("apps.accounts.serializers.signup_serializer.cache")
    def test_signup_invalid_token(self, mock_serializer_cache) -> None:
        mock_serializer_cache.get.return_value = None
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "email_token": "valid-token",
                "nickname": "newuser",
                "password": "Test@1234",
                "password_confirm": "Test@1234",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("apps.accounts.serializers.signup_serializer.cache")
    @patch("apps.accounts.service.signup_service.cache")
    def test_signup_invalid_password(self, mock_cache, mock_serializer_cache) -> None:
        mock_cache.get.return_value = {"email": "test2@test.com"}
        mock_serializer_cache.get.return_value = {"email": "test2@test.com"}
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "email_token": "valid-token",
                "nickname": "newuser",
                "password": "Test@1234",
                "password_confirm": "Wrong@1234",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("apps.accounts.serializers.signup_serializer.cache")
    @patch("apps.accounts.service.signup_service.cache")
    def test_signup_invalid_nickname(self, mock_cache, mock_serializer_cache) -> None:
        mock_cache.get.return_value = {"email": "test@test.com"}
        mock_serializer_cache.get.return_value = {"email": "test@test.com"}
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "email_token": "valid-token",
                "nickname": "test",
                "password": "Test@1234",
                "password_confirm": "Test@1234",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("apps.accounts.serializers.signup_serializer.cache")
    @patch("apps.accounts.service.signup_service.cache")
    def test_signup_email_none(self, mock_cache, mock_serializer_cache) -> None:
        mock_cache.get.return_value = None
        mock_serializer_cache.get.return_value = {"email": "test@test.com"}
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "email_token": "valid-token",
                "nickname": "newuser",
                "password": "Test@1234",
                "password_confirm": "Test@1234",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("apps.accounts.serializers.signup_serializer.cache")
    @patch("apps.accounts.service.signup_service.cache")
    def test_signup_email_data_none(self, mock_cache, mock_serializer_cache) -> None:
        mock_cache.get.return_value = {"email": None}
        mock_serializer_cache.get.return_value = {"email": "test@test.com"}
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "email_token": "valid-token",
                "nickname": "newuser",
                "password": "Test@1234",
                "password_confirm": "Test@1234",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("apps.accounts.serializers.signup_serializer.cache")
    @patch("apps.accounts.service.signup_service.cache")
    def test_nickname_already_registered(self, mock_cache, mock_serializer_cache) -> None:
        mock_cache.get.return_value = {"email": "test2@test.com"}
        mock_serializer_cache.get.return_value = {"email": "test2@test.com"}

        response = self.client.post(
            reverse("accounts:signup"),
            {
                "email_token": "valid-token",
                "nickname": "test",
                "password": "Test@1234",
                "password_confirm": "Test@1234",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

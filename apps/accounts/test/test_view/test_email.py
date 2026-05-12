from unittest.mock import patch

from django.urls import reverse
from redis import RedisError
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


class EmailSendViewTest(BaseViewTest):

    def setUp(self) -> None:
        super().setUp()
        self.cache_patcher = patch("apps.accounts.service.email_service.cache")
        self.send_mail_patcher = patch("apps.accounts.service.email_service.send_mail")

        self.mock_cache = self.cache_patcher.start()
        self.mock_send_mail = self.send_mail_patcher.start()

        self.addCleanup(self.cache_patcher.stop)
        self.addCleanup(self.send_mail_patcher.stop)

    def test_send_email_success(self) -> None:
        self.mock_cache.set.return_value = None
        self.mock_send_mail.return_value = None
        response = self.client.post(
            reverse("accounts:email-send"),
            {
                "email": "test@test.com",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_send_email_error(self) -> None:
        self.mock_cache.set.return_value = None
        self.mock_send_mail.return_value = None
        response = self.client.post(
            reverse("accounts:email-send"),
            {
                "email": "testtest.com",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_email_invalid_token(self) -> None:
        self.mock_cache.set.return_value = None
        self.mock_send_mail.side_effect = Exception("SMTP error")
        response = self.client.post(
            reverse("accounts:email-send"),
            {
                "email": "test@test.com",
            },
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_email_redis_error(self) -> None:
        self.mock_cache.set.side_effect = RedisError("redis error")

        response = self.client.post(reverse("accounts:email-send"), {"email": "test@test.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EmailVerifyViewTest(BaseViewTest):
    def setUp(self) -> None:
        super().setUp()
        self.cache_patcher = patch("apps.accounts.service.email_service.cache")
        self.mock_cache = self.cache_patcher.start()
        self.addCleanup(self.cache_patcher.stop)

    def test_verify_email_success(self) -> None:
        self.mock_cache.get.return_value = "123456"

        response = self.client.post(
            reverse("accounts:email-verify"),
            {
                "email": "test@test.com",
                "code": "123456",
            },
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expire_verify_email_error(self) -> None:
        self.mock_cache.get.return_value = None
        response = self.client.post(
            reverse("accounts:email-verify"),
            {
                "email": "test@test.com",
                "code": "123456",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_code_wrong_email_error(self) -> None:
        self.mock_cache.get.return_value = "123456"
        response = self.client.post(
            reverse("accounts:email-verify"),
            {
                "email": "test@test.com",
                "code": "123455",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cache_data_email_error(self) -> None:
        self.mock_cache.get.side_effect = RedisError("redis error")
        response = self.client.post(
            reverse("accounts:email-verify"),
            {
                "email": "test@test.com",
                "code": "123455",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_redis_email_error(self) -> None:
        self.mock_cache.get.return_value = "123456"
        self.mock_cache.set.side_effect = RedisError("redis error")
        response = self.client.post(
            reverse("accounts:email-verify"),
            {
                "email": "test@test.com",
                "code": "123456",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

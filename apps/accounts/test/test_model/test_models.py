from django.test import TestCase

from apps.accounts.models.signup_models import Account


class UserModelTest(TestCase):

    def setUp(self) -> None:
        self.account = Account.objects.create_user(
            email="test@test.com",
            password="testpassword",
            nickname="test",
        )

    def test_create_account(self) -> None:

        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(self.account.email, "test@test.com")
        self.assertTrue(self.account.check_password("testpassword"))
        self.assertEqual(self.account.nickname, "test")
        self.assertFalse(self.account.is_active)

    def test_create_superuser(self) -> None:
        self.super = Account.objects.create_superuser(
            email="super@test.com",
            password="Super@1234",
            nickname="super",
        )
        self.assertEqual(self.super.email, "super@test.com")
        self.assertTrue(self.super.check_password("Super@1234"))
        self.assertEqual(self.super.nickname, "super")
        self.assertTrue(self.super.is_active)
        self.assertTrue(self.super.is_staff)
        self.assertTrue(self.super.is_superuser)

    def test_duplicate_email_error(self) -> None:
        with self.assertRaises(Exception):
            Account.objects.create_user(
                email="test@test.com",
                password="testpassword2",
                nickname="test2",
            )

    def test_duplicate_nickname_error(self) -> None:
        with self.assertRaises(Exception):
            Account.objects.create_user(
                email="test2@test.com",
                password="testpassword2",
                nickname="test",
            )

    def test_str(self) -> None:
        self.assertEqual(str(self.account), "test@test.com")

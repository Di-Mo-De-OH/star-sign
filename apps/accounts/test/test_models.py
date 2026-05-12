from django.test import TestCase

from apps.accounts.model.signup_models import Account, SocialAccount


class AccountTest(TestCase):
    """
    Test Account Model
    """

    account: Account

    def setUp(self) -> None:
        self.account = Account.objects.create_user(
            email="test@test.com",
            password="testpassword",
            nickname="testnickname",
        )

    def test_create_account(self) -> None:
        """check account model create"""

        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(self.account.email, "test@test.com")
        self.assertEqual(self.account.nickname, "testnickname")
        self.assertFalse(self.account.is_active)
        self.assertFalse(self.account.is_email_verified)
        self.assertFalse(self.account.is_staff)

    def test_password_is_hashed(self) -> None:
        """check password is hashed"""
        self.assertTrue(self.account.check_password("testpassword"))

    def test_duplicate_email_error(self) -> None:
        """check duplicate email"""
        with self.assertRaises(Exception):
            Account.objects.create_user(
                email="test@test.com",
                password="testpassword",
                nickname="testnickname2",
            )

    def test_duplicate_nickname_error(self) -> None:
        """check duplicate nickname"""
        with self.assertRaises(Exception):
            Account.objects.create_user(
                email="test2@test.com",
                password="testpassword",
                nickname="testnickname",
            )

    def test_create_superuser(self) -> None:
        """check superuser model create"""
        self.superuser = Account.objects.create_superuser(
            email="testsuperuser@test.com",
            password="testpassword",
            nickname="superuser",
        )
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(self.superuser.email, "testsuperuser@test.com")
        self.assertEqual(self.superuser.nickname, "superuser")
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_superuser)
        self.assertTrue(self.superuser.is_staff)
        self.assertFalse(self.superuser.is_email_verified)

    def test_str(self) -> None:
        """check string representation"""
        self.assertEqual(str(self.account), self.account.email)


class SocialAccountTest(TestCase):
    """
    Test SocialAccount Model
    """

    def setUp(self) -> None:
        self.account = Account.objects.create_user(
            email="test@test.com",
            password="testpassword",
            nickname="testnickname",
        )

    def test_create_social_account(self) -> None:
        """create social account"""
        self.social_account = SocialAccount.objects.create(
            user=self.account,
            provider="google",
            provider_id="google-uid-123",
        )
        self.assertEqual(SocialAccount.objects.count(), 1)
        self.assertEqual(self.social_account.provider, "google")
        self.assertEqual(self.social_account.provider_id, "google-uid-123")
        self.assertEqual(self.social_account.user, self.account)

    def test_unique_together_error(self) -> None:
        """check duplicate provider + provider_id raises error"""
        SocialAccount.objects.create(
            user=self.account,
            provider="google",
            provider_id="google-uid-123",
        )
        with self.assertRaises(Exception):
            SocialAccount.objects.create(
                user=self.account,
                provider="google",
                provider_id="google-uid-123",
            )

    def test_cascade_delete(self) -> None:
        """check social account deleted when account deleted"""
        SocialAccount.objects.create(
            user=self.account,
            provider="google",
            provider_id="google-uid-123",
        )
        self.account.delete()
        self.assertEqual(SocialAccount.objects.count(), 0)

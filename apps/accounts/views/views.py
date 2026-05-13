from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers.email_serializer import EmailSendSerializer, EmailVerifySerializer
from apps.accounts.serializers.login_serializers import LoginRequestSerializer
from apps.accounts.serializers.signup_serializer import AccountResponseSerializer, SignUpRequestSerializer
from apps.accounts.service.email_service import EmailSendService
from apps.accounts.service.login_logout_service import LoginService, LogoutService
from apps.accounts.service.signup_service import SignUpService


class EmailSendView(APIView):
    """
    POST api/v1/accounts/email/send/
    Send verification code to the given email address.
    """

    permission_classes = [
        AllowAny,
    ]
    service = EmailSendService()

    def post(self, request: Request) -> Response:
        serializer = EmailSendSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.service.send_email(
            serializer.validated_data["email"],
        )
        return Response({"detail": "email send"}, status=status.HTTP_200_OK)


class EmailVerifyView(APIView):
    """
    POST api/v1/accounts/email/verify/
    Verify the code sent to the given email address.
    """

    permission_classes = [
        AllowAny,
    ]
    service = EmailSendService()

    def post(self, request: Request) -> Response:
        serializer = EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verify_token = self.service.verify_code(serializer.validated_data["email"], serializer.validated_data["code"])
        return Response(
            {
                "detail": "email verified",
                "email_token": verify_token,
            },
            status=status.HTTP_200_OK,
        )


class SignUpView(APIView):
    """
    POST api/v1/accounts/signup/
    Create a new user
    """

    permission_classes = [
        AllowAny,
    ]
    service = SignUpService()

    def post(self, request: Request) -> Response:
        serializer = SignUpRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = self.service.create_user(serializer.validated_data)
        return Response(
            {"detail": "user created", "account": AccountResponseSerializer(account).data},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    POST api/v1/accounts/login/
    Authenticate user and return JWT tokens.
    """

    permission_classes = [
        AllowAny,
    ]
    service = LoginService()

    def post(self, request: Request) -> Response:
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_refresh_token = request.COOKIES.get("refresh_token")

        access_token, refresh_token = self.service.login(
            serializer.validated_data["email"],
            serializer.validated_data["password"],
            old_refresh_token,
        )

        response = Response(
            {"detail": "user logged in", "access_token": access_token},
            status=status.HTTP_200_OK,
        )
        response.set_cookie("refresh_token", refresh_token, httponly=True)

        return response


class LogoutView(APIView):
    """
    POST api/v1/accounts/logout/
    Invalidate refresh token and clear cookie.
    """

    permission_classes = [
        IsAuthenticated,
    ]
    service = LogoutService()

    def post(self, request: Request) -> Response:

        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            raise ValidationError("Refresh token is required")

        self.service.logout(refresh_token)
        response = Response(
            {
                "detail": "user logged out",
            },
            status=status.HTTP_200_OK,
        )

        response.delete_cookie("refresh_token")
        return response

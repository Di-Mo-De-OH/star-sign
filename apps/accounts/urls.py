from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.views import views

app_name = "accounts"

urlpatterns = [
    path("email/send", views.EmailSendView.as_view(), name="email-send"),
    path("email/verify", views.EmailVerifyView.as_view(), name="email-verify"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

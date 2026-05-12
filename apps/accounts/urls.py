from django.urls import path

from apps.accounts.views import views

app_name = "accounts"

urlpatterns = [
    path("email/send", views.EmailSendView.as_view(), name="email-send"),
    path("email/verify", views.EmailVerifyView.as_view(), name="email-verify"),
    path("signup", views.SignUpView.as_view(), name="signup"),
]

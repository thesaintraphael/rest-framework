from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="registration"),
    path("login/", views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("verify-email/", views.VerifyEmail.as_view(), name="verify-email"),
    path("verify-code/", views.VerifyCodeView.as_view(), name="verify-code"),
    path("reset-password-request/", views.ResetPasswordMailView.as_view(), name="reset-password-mail"),
    path("reset-password-complete/", views.ResetPasswordCompleteView.as_view(), name="reset-password-complete"),
]

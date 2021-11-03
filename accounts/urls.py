from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="registration"),
    path("verify-email/", views.VerifyEmail.as_view(), name="verify-email"),
]

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from products.utils import SerializerUtil
from .renderers import UserRenderer
from .models import User
from .serializers import (LoginSerializer, LogoutSerializer, RegistrationSerializer, CodeSerializer,
                          ResetPasswordCompleteSerializer, ResetPasswordSerializer, VerifyCodeSerializer)
from .utils import send_email


class RegistrationView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer
    renderer_classes = (UserRenderer, )
    # It is also possible to set a default renderer
    #  from Rest Fr settings in settings.py

    def post(self, request):

        serializer = SerializerUtil(
            self.serializer_class).save_serializer(data=request.data)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        send_email(email, user.activation_code)

        return Response({"message": "Verification code is sent to your email address"})


class VerifyEmail(generics.GenericAPIView):

    serializer_class = CodeSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(
            activation_code=serializer.validated_data['code']).first()
        user.activation_code = None
        user.is_verified = True
        user.save()
        tokens = user.tokens

        return Response({"message": "Successfully activated", "tokens": tokens})


class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user(request.data['email'])

        return Response({'tokens': user.tokens})


class LogoutView(generics.GenericAPIView):

    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        self.serializer_class(
            data=request.data).is_valid(raise_exception=True)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ResetPasswordMailView(generics.GenericAPIView):

    serializer_class = ResetPasswordSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_reset_mail(serializer.validated_data['email'])

        return Response({"Code is sent to your email"})


class VerifyCodeView(generics.GenericAPIView):

    serializer_class = VerifyCodeSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"code": serializer.validated_data['code']})


class ResetPasswordCompleteView(generics.GenericAPIView):

    serializer_class = ResetPasswordCompleteSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.get_tokens(serializer.validated_data)

        return Response({
            "tokens": tokens,
        })

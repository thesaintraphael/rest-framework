from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.tokens import RefreshToken


from .models import User
from .serializers import RegistrationSerializer, CodeSerializer
from .utils import send_email


class RegistrationView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        serializer.save()

        user = User.objects.get(email=email)
        send_email(email, user.activation_code)

        return Response({"message": "Verification code is sent to your email address"})


class VerifyEmail(generics.GenericAPIView):

    serializer_class = CodeSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(activation_code=serializer.validated_data['code']).first()
        user.activation_code = None
        user.save()
        tokens = user.tokens

        return Response({"message": "Successfully activated", "tokens": tokens})

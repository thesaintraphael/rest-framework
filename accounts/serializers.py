from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .utils import create_act_code, send_email


CODE_TYPE = {
    ("act_code", "act_code"),
    ("reset_code", "reset_code")
}


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, min_length=6
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):

        email = attrs.get("email")
        user = User.objects.filter(email=email).exists()

        if user and user.is_verified:
            raise AuthenticationFailed(
                "User with this email is already exist", "401")

        first_isalpha = attrs["password"][0].isalpha()
        if all(first_isalpha == character.isalpha() for character in attrs["password"]):
            raise serializers.ValidationError(
                {"error": "Password must be consis of at least one digit and letters"}
            )

        return attrs

    def create(self, validated_data):

        data = validated_data

        user = User.objects.create(
            username=data["username"],
            email=data["email"],
        )

        user.set_password(data["password"])
        user.activation_code = create_act_code()
        user.save()

        return user


class CodeSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=6, min_length=6)

    def validate(self, attrs):
        code = attrs['code']

        users = User.objects.filter(activation_code=code)
        if users.exists():
            return attrs

        raise AuthenticationFailed("Wrong code",  "401")


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    def validate(self, attrs):

        users = User.objects.filter(email=attrs['email'])

        if users.exists():
            user = users.first()
            if not user.is_verified:
                raise AuthenticationFailed("Email is not verified", '401')
            if user.check_password(attrs['password']):
                return attrs

        raise AuthenticationFailed(
            'Wrong password email combination', '401')

    def get_user(self, email):

        return User.objects.get(email=email)


class LogoutSerializer(serializers.Serializer):

    refresh_token = serializers.CharField()

    default_error_message = {
        'bad_token': ("Token is expired or invalid")
    }

    def validate(self, attrs):

        try:
            token = RefreshToken(attrs['refresh_token'])
            token.blacklist()

        except TokenError as e:
            raise ValidationError({'error': "Invalid or expired token"}) from e

        return attrs


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate(self, attrs):

        users = User.objects.filter(email=attrs['email'])
        if not users:
            raise AuthenticationFailed('No user with such an email', "401")

        return attrs

    def send_reset_mail(self, email):

        user = User.objects.get(email=email)
        user.reset_code = create_act_code(code_type="reset_code")
        user.save()

        send_email(email, user.reset_code)


class VerifyCodeSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=6, min_length=6)

    def validate(self, attrs):
        code = attrs['code']

        users = User.objects.filter(reset_code=code)
        if users.exists():
            return attrs

        raise AuthenticationFailed("Wrong code",  "401")


class ResetPasswordCompleteSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=6)
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, min_length=6
    )
    password_confirm = serializers.CharField(
        style={"input_type": "password"}, write_only=True, min_length=6
    )

    def validate(self, attrs):

        users = User.objects.filter(reset_code=attrs['code'])
        if not users.exists():
            raise AuthenticationFailed("Wrong code", "401")

        password1 = attrs['password']
        password2 = attrs['password_confirm']

        if password2 != password1:
            raise serializers.ValidationError(
                {"error": "Passwords are not same"})

        first_isalpha = password1[0].isalpha()
        if all(first_isalpha == character.isalpha() for character in password1):
            raise serializers.ValidationError(
                {"error": "Password should contain numbers and letters"})

        return attrs

    def get_tokens(self, attrs):

        user = User.objects.filter(reset_code=attrs['code']).first()
        user.reset_code = None
        user.save()

        return user.tokens

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .utils import create_act_code


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
            if user.check_password(attrs['password']):
                return attrs

        raise AuthenticationFailed(
            'Wrong password email combination', '401')

    def get_user(self, email):

        return User.objects.get(email=email)

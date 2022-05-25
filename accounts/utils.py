from django.core.mail import EmailMessage
from django.conf import settings

from .models import User

import string
import random


class UserCodeUtil:

    _size = 6

    @staticmethod
    def generate_code() -> str:
        return ''.join(random.choice(string.digits) for _ in range(UserCodeUtil._size))

    @staticmethod
    def create_act_code() -> str:
        code = UserCodeUtil.generate_code()
        if User.objects.filter(activation_code=code).exists():
            return UserCodeUtil.create_act_code()

        return code

    @staticmethod
    def create_reset_code() -> str:
        code = UserCodeUtil.generate_code()
        if User.objects.filter(reset_code=code).exists():
            return UserCodeUtil.create_reset_code()

        return code


def send_email(email, code) -> None:

    email = EmailMessage(
        'Email Verification', f'Code {code}',
        settings.EMAIL_HOST_USER, [email]
    )

    email.send()

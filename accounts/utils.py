from django.core.mail import EmailMessage
from django.conf import settings

from .models import User

import string
import random


class UserCodeUtil:

    _size = 6

    @staticmethod
    def generate_code(chars=string.digits):
        return ''.join(random.choice(chars) for _ in range(UserCodeUtil._size))

    @staticmethod
    def create_act_code():
        code = UserCodeUtil.generate_code()
        if User.objects.filter(activation_code=code).exists():
            return UserCodeUtil.create_act_code()

        return code

    @staticmethod
    def create_reset_code():
        code = UserCodeUtil.generate_code()
        if User.objects.filter(reset_code=code).exists():
            return UserCodeUtil.create_reset_code()

        return code


def send_email(email, code):

    email = EmailMessage(
        'Email Verification', f'Code {code}',
        settings.EMAIL_HOST_USER, [email]
    )

    email.send()

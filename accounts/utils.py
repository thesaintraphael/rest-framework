from django.core.mail import EmailMessage
from django.conf import settings

from .models import User

import string
import random


class UserCodeUtil:

    def __init__(self, size=6) -> None:
        """Allowing to set a different size of code if needed"""
        self.size = size

    @staticmethod
    def generate_code(size: int) -> str:
        return ''.join(random.choice(string.digits) for _ in range(size))

    def create_act_code(self) -> str:
        code = self.generate_code(self.size)
        if User.objects.filter(activation_code=code).exists():
            return self.create_act_code()

        return code

    def create_reset_code(self) -> str:
        code = self.generate_code(self.size)
        if User.objects.filter(reset_code=code).exists():
            return self.create_reset_code()

        return code


def send_email(email, code) -> None:

    email = EmailMessage(
        'Email Verification', f'Code {code}',
        settings.EMAIL_HOST_USER, [email]
    )

    email.send()

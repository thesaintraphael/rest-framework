from django.core.mail import EmailMessage
from django.conf import settings

from .models import User

import string
import random


def generate_code(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_act_code(size=6):
    code = generate_code(size)
    code_exists = User.objects.filter(activation_code=code).exists()

    if code_exists:
        return create_act_code(size)
    return code


def send_email(email, code):

    email = EmailMessage(
        'Email Verification', f'Code {code}',
        settings.EMAIL_HOST_USER, [email]
    )

    email.send()

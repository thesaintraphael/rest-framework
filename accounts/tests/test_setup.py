from django.urls import reverse
from rest_framework.test import APITestCase
from faker import Faker


class TestSetup(APITestCase):

    def setUp(self) -> None:

        self.register_url = reverse('registration')
        self.login_url = reverse('login')
        self.fake = Faker()
        self.user_data = {
            "email": self.fake.email(),
            'username': self.fake.email().split("@")[0],
            'password': self.fake.email(),
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

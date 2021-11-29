from .test_setup import TestSetup
from ..models import User


class TestView(TestSetup):

    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 400)

    def test_user_can_register_correctly(self):
        response = self.client.post(
            self.register_url, self.user_data, format='json'
        )

        self.assertEqual(response.status_code, 200)

    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(
            self.register_url, self.user_data, format="json")
        response = self.client.post(
            self.login_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_user_can_login_after_verification(self):
        self.client.post(
            self.register_url, self.user_data, format="json")
        email = self.user_data.get('email')
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)

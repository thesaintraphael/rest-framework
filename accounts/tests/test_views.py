from unittest.mock import patch

from .test_setup import TestSetup
from ..models import User


class TestView(TestSetup):

    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 400)

    @patch("accounts.views.send_email")
    def test_user_can_register_correctly(self, mock_email):
        response = self.client.post(
            self.register_url, self.user_data, format='json'
        )

        self.assertEqual(response.status_code, 200)
        mock_email.assert_called_once()

    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(
            self.register_url, self.user_data, format="json")
        response = self.client.post(
            self.login_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 401)

    @patch("accounts.views.send_email")
    def test_user_can_login_after_verification(self, mock_email):
        self.client.post(
            self.register_url, self.user_data, format="json")
        
        email = self.user_data.get('email')
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)

        mock_email.assert_called_with(
            self.user_data['email'], user.activation_code)

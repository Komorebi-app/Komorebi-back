from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

class TestToken(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.url = "/api/token/"
        self.user_1 = User.objects.create_user(username = "Test", password = "Password")

    def test_should_return_a_token(self):
        data = {"username": "Test", "password": "Password"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIsInstance(response.data["access"], str)
        self.assertIsInstance(response.data["refresh"], str)

    def test_should_return_an_error_if_password_doesnt_match(self):
        data = {"username": "Test", "password": "Password2"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 401)

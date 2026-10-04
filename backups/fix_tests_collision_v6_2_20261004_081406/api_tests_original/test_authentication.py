from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from django.urls import reverse


User = get_user_model()


class AuthenticationAPITests(APITestCase):

    def test_register(self):

        response = self.client.post(
            reverse("api-register"),
            {
                "username": "test_nsikay_auth",
                "email": "auth@nsikay.test",
                "first_name": "Test",
                "last_name": "NSIKAY",
                "password": "NsikayTest123!",
                "password_confirm": "NsikayTest123!",
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            201
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertIn(
            "token",
            response.data
        )

        self.assertTrue(
            User.objects.filter(
                username="test_nsikay_auth"
            ).exists()
        )

    def test_login(self):

        User.objects.create_user(
            username="login_nsikay",
            email="login@nsikay.test",
            password="NsikayTest123!"
        )

        response = self.client.post(
            reverse("api-login"),
            {
                "username": "login_nsikay",
                "password": "NsikayTest123!",
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertIn(
            "token",
            response.data
        )

    def test_login_invalid(self):

        response = self.client.post(
            reverse("api-login"),
            {
                "username": "inconnu_nsikay",
                "password": "incorrect",
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            401
        )

    def test_me_requires_authentication(self):

        response = self.client.get(
            reverse("api-me")
        )

        self.assertEqual(
            response.status_code,
            401
        )

    def test_me_authenticated(self):

        user = User.objects.create_user(
            username="me_nsikay",
            email="me@nsikay.test",
            password="NsikayTest123!"
        )

        token = Token.objects.create(
            user=user
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        response = self.client.get(
            reverse("api-me")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertEqual(
            response.data["user"]["username"],
            "me_nsikay"
        )

    def test_logout(self):

        user = User.objects.create_user(
            username="logout_nsikay",
            email="logout@nsikay.test",
            password="NsikayTest123!"
        )

        token = Token.objects.create(
            user=user
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        response = self.client.post(
            reverse("api-logout")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertFalse(
            Token.objects.filter(
                user=user
            ).exists()
        )

    def test_profile_requires_authentication(self):

        response = self.client.get(
            reverse("api-profile")
        )

        self.assertEqual(
            response.status_code,
            401
        )

    def test_profile_authenticated(self):

        user = User.objects.create_user(
            username="profile_nsikay",
            email="profile@nsikay.test",
            password="NsikayTest123!"
        )

        token = Token.objects.create(
            user=user
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        response = self.client.get(
            reverse("api-profile")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data["user"]["username"],
            "profile_nsikay"
        )


class ExistingAPIEndpointTests(APITestCase):

    def test_users_endpoint(self):

        response = self.client.get(
            reverse("api-users")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_banks_endpoint(self):

        response = self.client.get(
            reverse("api-banks")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_countries_endpoint(self):

        response = self.client.get(
            reverse("api-countries")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_certifications_endpoint(self):

        response = self.client.get(
            reverse("api-certifications")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_transactions_endpoint(self):

        response = self.client.get(
            reverse("api-transactions")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_finance_endpoint(self):

        response = self.client.get(
            reverse("api-finance")
        )

        self.assertEqual(
            response.status_code,
            200
        )

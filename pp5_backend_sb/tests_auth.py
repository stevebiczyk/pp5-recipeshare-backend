
from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="StrongTestPassword123!",
        )

    def test_login_sets_jwt_cookies(self):
        response = self.client.post(
            "/dj-rest-auth/login/",
            {
                "username": "testuser",
                "password": "StrongTestPassword123!",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn("my-app-auth", response.cookies)
        self.assertIn("my-refresh-token", response.cookies)
        self.assertTrue(
            response.cookies["my-app-auth"]["httponly"]
        )

    def test_authenticated_user_endpoint(self):
        self.client.post(
            "/dj-rest-auth/login/",
            {
                "username": "testuser",
                "password": "StrongTestPassword123!",
            },
        )

        response = self.client.get("/dj-rest-auth/user/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["username"],
            "testuser",
        )

    def test_refresh_sets_new_access_cookie(self):
        self.client.post(
            "/dj-rest-auth/login/",
            {
                "username": "testuser",
                "password": "StrongTestPassword123!",
            },
        )

        response = self.client.post(
            "/dj-rest-auth/token/refresh/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn("my-app-auth", response.cookies)

    def test_logout_clears_authentication(self):
        self.client.post(
            "/dj-rest-auth/login/",
            {
                "username": "testuser",
                "password": "StrongTestPassword123!",
            },
        )

        response = self.client.post("/dj-rest-auth/logout/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        user_response = self.client.get("/dj-rest-auth/user/")
        self.assertIn(user_response.status_code, (401, 403))

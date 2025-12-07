from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from users.models import Profile

User = get_user_model()


class UsersTestCase(TestCase):
    def test_user_creation_creates_profile(self):
        user = User.objects.create_user(email="test@example.com", password="pass")
        self.assertIsNotNone(user.profile)
        self.assertEqual(str(user.profile), f"{user.email} Profile")

    def test_register_serializer(self):
        user = User.objects.create_user(email="serializer@example.com", password="pass")
        self.assertEqual(user.email, "serializer@example.com")

    def test_register_api_view(self):
        """Проверка DRF API регистрации."""
        url = "/api/register/"  # путь к CreateAPIView
        data = {
            "email": "apiviewuser@example.com",
            "password": "pass123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="apiviewuser@example.com")
        self.assertIsNotNone(user.profile)
        self.assertTrue(user.check_password("pass123"))

    def test_user_str_and_profile_str(self):
        """Проверка __str__ методов моделей."""
        user = User.objects.create_user(email="test@example.com", password="pass")
        profile = user.profile

        # Проверяем, что __str__ пользователя возвращает email
        self.assertEqual(str(user), user.email)

        profile.telegram_chat_id = "123456"
        # Проверяем, что __str__ профиля возвращает email пользователя + "Profile"
        self.assertEqual(str(profile), f"{user.email} Profile")

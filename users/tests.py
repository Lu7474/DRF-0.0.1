from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class UserViewSetTests(TestCase):
    def setUp(self):
        """Настройка тестового окружения"""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.superuser = User.objects.create_superuser(
            username="admin", password="adminpass"
        )

    def test_register_user(self):
        """Тест регистрации нового пользователя"""
        data = {"username": "newuser", "password": "newpass"}
        response = self.client.post("/api/v1/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_get_users_list_as_user(self):
        """Обычный пользователь должен видеть только себя"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], self.user.username)

    def test_get_users_list_as_admin(self):
        """Администратор должен видеть всех пользователей"""
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_get_user_detail(self):
        """Пользователь должен видеть только свой профиль"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/v1/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_update_user(self):
        """Пользователь должен иметь возможность обновлять свой профиль"""
        self.client.force_authenticate(user=self.user)
        data = {"username": "updateduser"}
        response = self.client.patch(f"/api/v1/users/{self.user.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")

    def test_delete_user(self):
        """Пользователь должен иметь возможность удалить себя"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/v1/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

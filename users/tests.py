from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserManagerTestCase(TestCase):
    """Тесты кастомного менеджера пользователей."""

    def test_create_user_without_email(self) -> None:
        """Тест создания пользователя без email."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="testpass123")

    def test_create_superuser_is_staff_false(self) -> None:
        """Тест создания суперпользователя с is_staff=False."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@test.com", password="testpass123", is_staff=False
            )

    def test_create_superuser_is_superuser_false(self) -> None:
        """Тест создания суперпользователя с is_superuser=False."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@test.com", password="testpass123", is_superuser=False
            )


class UserModelTestCase(TestCase):
    """Тесты модели пользователя."""

    def test_create_user(self) -> None:
        user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual(str(user), "test@example.com")

    def test_create_superuser(self) -> None:
        admin_user = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_optional_fields(self) -> None:
        """Тест необязательных полей пользователя."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            phone="+79999999999",
            city="Moscow",
        )
        self.assertEqual(user.phone, "+79999999999")
        self.assertEqual(user.city, "Moscow")

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from bookmarker.models import UserManager


class UserCreationTests(TestCase):
    user_model = get_user_model()
    user_manager = UserManager

    def test_create_user(self):
        user = self.user_model.objects.create_user("test@example.com", "12345")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_confirmed)

        with self.assertRaises(IntegrityError):
            self.user_model.objects.create_user("test@example.com", "67890")

        with self.assertRaises(TypeError):
            self.user_model.objects.create_user()
        with self.assertRaises(ValueError):
            self.user_model.objects.create_user("", "")
        with self.assertRaises(ValueError):
            self.user_model.objects.create_user("test1@example.com", "")
        with self.assertRaises(ValueError):
            self.user_model.objects.create_user("", "12345")

    def test_create_superuser(self):
        user = self.user_model.objects.create_superuser("test@example.com", "12345")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_confirmed)

        with self.assertRaises(IntegrityError):
            self.user_model.objects.create_superuser("test@example.com", "67890")

        with self.assertRaises(TypeError):
            self.user_model.objects.create_superuser()
        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser("", "")
        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser("test1@example.com", "")
        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser("", "12345")

        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser(
                "test@example.com", "12345", is_staff=False
            )
        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser(
                "test@example.com", "12345", is_superuser=False
            )

    def test_manager(self):
        self.assertEqual(self.user_manager, type(self.user_model.objects))

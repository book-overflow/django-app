from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserManagerTests(TestCase):
    def test_create_user(self):
        manager = get_user_model().objects
        email = "test@example.com"
        password = "testpassword"
        user = manager.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        manager = get_user_model().objects
        email = "admin@example.com"
        password = "adminpassword"
        superuser = manager.create_superuser(email=email, password=password)

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_superuser)


class CustomUserModelTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="test@example.com", password="testpassword"
        )

        self.assertEqual(user.email, "test@example.com")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_superuser)

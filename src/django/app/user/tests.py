print("hello world")

from django.test import TestCase
from django.contrib.auth import get_user_model
from user.models import CustomUser, CustomUserManager


class CustomUserManagerTests(TestCase):

    def test_create_user(self):
        """Test creating a user with an email is successful"""
        User = CustomUser()
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            date_of_birth="1990-01-01",
            phone_number="1234567890",
            street="123 Main St",
            city="Anytown",
            state="TX",  # Assuming STATE_CHOICES is defined in your models.py
            zip="12345",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

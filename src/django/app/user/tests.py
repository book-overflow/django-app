from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import STATE_CHOICES  # Import your STATE_CHOICES if needed
from unittest.mock import patch
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class CustomUserManagerTests(TestCase):
    def test_create_user(self):
        """Test creating a user with email is successful"""
        User = get_user_model()
        user = User.objects.create_user(
            email="test@nyu.edu",
            password="password",
            first_name="Test",
            last_name="User",
            date_of_birth="1999-01-01",
            phone_number="1234567890",
            street="123 Main St",
            city="Anytown",
            state="TX",
            zip="12345",
            is_staff=False,
            is_active=True,
        )
        self.assertEqual(user.email, "test@nyu.edu")
        self.assertTrue(user.check_password("password"))
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        """Test creating a superuser is successful"""
        User = get_user_model()
        superuser = User.objects.create_superuser(email="super@nyu.edu", password="foo")
        self.assertEqual(superuser.email, "super@nyu.edu")
        self.assertTrue(superuser.check_password("foo"))
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        User = get_user_model()
        email = "test@NYU.edu"
        # The line `user = User.objects.create_user(email, "test123")` is creating a new user object using the
        # custom user model's manager method `create_user`. This method is typically used to create a standard
        # user account with the provided email and password. In this case, the email is passed as the first
        # argument and the password "test123" as the second argument. The method will handle the normalization
        # of the email and password hashing internally before creating the user in the database.
        user = User.objects.create_user(email, "test123")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_user(None, "test123")

    def test_create_user_with_edu_email(self):
        """Test creating a user with an .edu email is successful"""
        User = get_user_model()
        user = User.objects.create_user(
            email="test@university.edu", password="testpass123"
        )
        self.assertEqual(user.email, "test@university.edu")

    def test_create_user_without_edu_email(self):
        """Test creating a user without an .edu email fails"""
        User = get_user_model()
        with self.assertRaises(ValidationError):
            User.objects.create_user(email="test@example.com", password="testpass123")


User = get_user_model()


class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            # Add other required fields
        }
        response = self.client.post("/register/", user_data)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email="test@example.com")
        self.assertFalse(user.is_active)


class UserRegistrationEmailTest(TestCase):
    @patch("django.core.mail.send_mail")
    def test_send_activation_email(self, mock_send_mail):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            # Add other required fields
        }
        self.client.post("/register/", user_data)
        self.assertTrue(mock_send_mail.called)
        args, kwargs = mock_send_mail.call_args
        self.assertIn("Activate your user account", kwargs["subject"])
        self.assertIn("test@example.com", kwargs["recipient_list"])


class UserActivationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123",
            is_active=False,
        )

    def test_activate_user_valid_token(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.get(f"/activate/{uidb64}/{token}/")
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_user_invalid_token(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        response = self.client.get(f"/activate/{uidb64}/invalid-token/")
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

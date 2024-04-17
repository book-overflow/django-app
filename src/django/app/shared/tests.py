from django.test import TestCase
from django.contrib.gis.geos import Point

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from .models import University, Student

User = get_user_model()


class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email="test@example.com", password="foo")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("foo"))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email="admin@example.com", password="foo"
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

    def test_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="foo")


class UniversityModelTest(TestCase):
    def test_creating_university(self):
        uni = University.objects.create(
            name="Test University", domain="testuni.edu", location=Point(1, 1)
        )
        self.assertEqual(uni.name, "Test University")
        self.assertIsInstance(uni.location, Point)


class StudentModelTest(TestCase):
    def setUp(self):
        self.university = University.objects.create(
            name="Example University", domain="example.edu", location=Point(5, 5)
        )

    def test_student_with_valid_domain(self):
        student = Student.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.edu",
            password="password123",
        )
        student.save()
        self.assertEqual(student._university, self.university)

    def test_student_with_invalid_domain(self):
        with self.assertRaises(ValidationError):
            Student.objects.create(
                first_name="Jane", last_name="Doe", email="jane@invalid.edu"
            )

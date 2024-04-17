from django.test import TestCase
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from student_profile.models import Profile
from shared.models import Student, University
from django.db import IntegrityError


# Create your tests here.
class ProfileModelTest(TestCase):
    def setUp(self):
        self.university = University.objects.create(
            name="Test University", domain="nyu.edu", location=Point(1, 1)
        )
        self.student = Student.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@nyu.edu",
            password="password1234",
        )

    def test_profile_creation(self):
        profile = Profile.objects.create(
            student=self.student,
            date_of_birth="1990-01-01",
            phone_number="1234567890",
            street="123 Main St",
            city="Anytown",
            state="NY",
            zip="12345",
            image="profile.png",  # Assuming 'profile.png' is correctly set up in your MEDIA_ROOT
        )
        self.assertEqual(profile.student, self.student)
        self.assertEqual(profile.city, "Anytown")

    def test_profile_with_null_fields(self):
        # Fields that can be null or blank should not raise any errors when left empty
        profile = Profile.objects.create(student=self.student)
        self.assertIsNone(profile.phone_number)
        self.assertIsNone(profile.city)

    def test_one_to_one_relationship(self):
        # Creating another profile for the same student should raise an IntegrityError
        Profile.objects.create(student=self.student)
        with self.assertRaises(IntegrityError):
            Profile.objects.create(student=self.student)

    def test_profile_deletion_cascade(self):
        # Ensure that deleting a student also deletes the associated profile
        profile = Profile.objects.create(student=self.student)
        self.student.delete()
        self.assertEqual(Profile.objects.filter(pk=profile.pk).count(), 0)

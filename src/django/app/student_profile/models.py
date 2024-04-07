from django.contrib.gis.db import models
from shared.models import Student

class Profile(models.Model):
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zip = models.CharField(max_length=5, null=True, blank=True)
    image = models.ImageField(default='profile.png', upload_to='profile/')
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="profile"
    )

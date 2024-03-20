from django.contrib.gis.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class University(CustomBaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.PointField()

class Student(CustomBaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    DOB = models.DateField()
    university = models.ForeignKey(University, on_delete=models.CASCADE)
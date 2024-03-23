# from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError


# GENERAL ______________________________________________________________________#
class CustomBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class CustomUser(CustomBaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

# UNIVERSITY MODEL _____________________________________________________________#
class University(CustomBaseModel):
    domain = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    location = models.PointField()

# STUDENT MODEL ________________________________________________________________#

class Student(CustomUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # ATTENTION: NEED TO REMOVE DEFAULT DATE OF BIRTH
    DOB = models.DateField(
        auto_now=False,
        auto_now_add=False,
        default=(timezone.now() - timedelta(days=18*365))
    )
    _university = models.ForeignKey(University, on_delete=models.CASCADE)
    
    def clean(self):
        pass

    def save(self, *args, **kwargs):
        domain = self.email.split("@")[1]
        try: 
            self._university = University.objects.get(domain=domain)
        except University.DoesNotExist:
            raise ValidationError("Invalid domain")
        
        self.full_clean()  # Performs full validation
        super().save(*args, **kwargs)
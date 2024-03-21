from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class University(CustomBaseModel):
    uniid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    # location = models.PointField()

# STUDENT MODEL ________________________________________________________________#
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        print(user)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
    
class Student(CustomBaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # DOB = models.DateField()
    # university = models.ForeignKey(University, on_delete=models.CASCADE)
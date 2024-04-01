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
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    date_of_birth = models.DateField(null=True, blank=True)
    _university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="students"
    )

#   To be moved to separate profile model    
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zip = models.CharField(max_length=5, null=True, blank=True)
    image = models.ImageField(default='profile.png', upload_to='profile/')
    
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

# COURSE MODEL _________________________________________________________________#
class Course(CustomBaseModel):
    course_number = models.CharField(max_length=255, primary_key=True)
    _university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField()

# TEXTBOOK MODEL _______________________________________________________________#
class Author(CustomBaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    
class Textbook(CustomBaseModel):
    isbn = models.PositiveBigIntegerField(primary_key=True)
    _authors = models.ManyToManyField(Author, related_name="textbooks")
    _belongs = models.ManyToManyField(Course, related_name="textbooks")
    
    name = models.CharField(max_length=255)
    edition = models.IntegerField()
    year_published = models.IntegerField()
    # image = models.ImageField(default='profile.png', upload_to='profile/')

class BookCondition(models.TextChoices):
    NEW = 'NEW', 'New'
    FINE = 'FINE', 'Fine'
    VERY_GOOD = 'VERY_GOOD', 'Very Good'
    GOOD = 'GOOD', 'Good'
    FAIR = 'FAIR', 'Fair'
    POOR = 'POOR', 'Poor'
    
class TextbookCopy(CustomBaseModel):
    _textbook = models.ForeignKey(
        Textbook,
        on_delete=models.CASCADE,
        related_name="copies"
    )
    _seller = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="copies"
    )
    
    condition = models.CharField(max_length=255, choices=BookCondition.choices)
    year_purchased = models.IntegerField()
    # image = models.ImageField(default='profile.png', upload_to='profile/')
    for_rent = models.BooleanField()
    for_sale = models.BooleanField()
    sale_price = models.DecimalField(max_digits=5, decimal_places=2)
    rent_price = models.DecimalField(max_digits=5, decimal_places=2)

# TRANSACTIONS _________________________________________________________________#
class TransactionStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    ONGOING = 'ONGOING', 'Ongoing'
    CANCELLED = 'CANCELLED', 'Cancelled'
    COMPLETED = 'COMPLETED', 'Completed'

class TransactionRating(models.TextChoices):
    BAD = 'BAD', 'Bad'
    AVERAGE = 'AVERAGE', 'Average'
    GOOD = 'GOOD', 'Good'
    EXCELLENT = 'EXCELLENT', 'Excellent'
    
class Transaction(CustomBaseModel):
    _buyer = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="purchases"
    )
    _seller = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="sales"
    )
    _textbook_copy = models.ForeignKey(
        TextbookCopy,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    
    for_sale = models.BooleanField()  
    price = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=255, choices=TransactionStatus.choices)

#   Rating attributes
    seller_rating_of_buyer = models.CharField(max_length=255, choices=TransactionRating.choices)
    seller_notes = models.TextField()
    buyer_rating_of_seller = models.CharField(max_length=255, choices=TransactionRating.choices)
    buyer_notes = models.TextField()
    
#   Renting attributes
    start_date = models.DateField()
    end_date = models.DateField()
    
    
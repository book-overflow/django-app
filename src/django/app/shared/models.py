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
            raise ValueError("User must have an email address.")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user


class CustomUser(CustomBaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"


# CHOICES ______________________________________________________________________#
class BookCondition(models.TextChoices):
    NEW = "NEW", "New"
    FINE = "FINE", "Fine"
    VERY_GOOD = "VERY_GOOD", "Very Good"
    GOOD = "GOOD", "Good"
    FAIR = "FAIR", "Fair"
    POOR = "POOR", "Poor"


class TransactionStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ONGOING = "ONGOING", "Ongoing"
    CANCELLED = "CANCELLED", "Cancelled"
    COMPLETED = "COMPLETED", "Completed"


class TransactionRating(models.TextChoices):
    BAD = "BAD", "Bad"
    AVERAGE = "AVERAGE", "Average"
    GOOD = "GOOD", "Good"
    EXCELLENT = "EXCELLENT", "Excellent"


# UNIVERSITY MODEL _____________________________________________________________#
class University(CustomBaseModel):
    domain = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    location = models.PointField()


# STUDENT MODEL ________________________________________________________________#
class Student(CustomUser):
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    _university = models.ForeignKey(
        University, on_delete=models.CASCADE, related_name="students"
    )

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

    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between."""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()


# COURSE MODEL _________________________________________________________________#
class Course(CustomBaseModel):
    course_number = models.CharField(max_length=255, primary_key=True)
    _university = models.ForeignKey(
        University, on_delete=models.CASCADE, related_name="courses"
    )

    name = models.CharField(max_length=255)
    description = models.TextField()


# TEXTBOOK MODEL _______________________________________________________________#
class Author(CustomBaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("first_name", "last_name")


class Textbook(CustomBaseModel):
    isbn = models.PositiveBigIntegerField(primary_key=True)
    _authors = models.ManyToManyField(Author, related_name="textbooks")
    _belongs = models.ManyToManyField(Course, related_name="textbooks")

    title = models.CharField(max_length=255)
    edition = models.IntegerField()
    # year_published = models.IntegerField()
    # image = models.ImageField(default='profile.png', upload_to='profile/')


class TextbookCopy(CustomBaseModel):
    _textbook = models.ForeignKey(
        Textbook, on_delete=models.CASCADE, related_name="copies"
    )
    _seller = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="copies"
    )

    condition = models.CharField(max_length=255, choices=BookCondition.choices)
    # year_purchased = models.IntegerField()
    image = models.ImageField(upload_to="books/")
    for_rent = models.BooleanField()
    for_sale = models.BooleanField()
    sale_price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    rent_price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # per month
    avail_from = models.DateField(null=True, blank=True)  # for rent only
    avail_to = models.DateField(null=True, blank=True)  # for rent only


# TRANSACTIONS _________________________________________________________________#
class Transaction(CustomBaseModel):
    _buyer = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="purchases"
    )
    _seller = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sales")
    _textbook_copy = models.ForeignKey(
        TextbookCopy, on_delete=models.CASCADE, related_name="transactions"
    )

    for_sale = models.BooleanField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=255, choices=TransactionStatus.choices)

    #   Rating attributes
    seller_rating_of_buyer = models.CharField(
        max_length=255, choices=TransactionRating.choices
    )
    seller_notes = models.TextField()
    buyer_rating_of_seller = models.CharField(
        max_length=255, choices=TransactionRating.choices
    )
    buyer_notes = models.TextField()

    #   Renting attributes
    start_date = models.DateField()
    end_date = models.DateField()

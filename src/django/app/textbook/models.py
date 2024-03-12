from django.contrib.auth.models import User
from django.db import models

class Textbook(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    

class Listing(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    course = models.DecimalField(max_digits=10, decimal_places=2)

    


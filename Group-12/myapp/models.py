from django.db import models

# Create your models here.
# Models are the way we interact with the database
class Listing(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField('date of listing')
    price = models.PositiveIntegerField()
    location = models.CharField(max_length=200)

class User(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    ACCOUNT_TYPES = {
        ('B', 'Buyer'),
        ('S', 'Seller'),
        ('A', 'Admin')
    }
    account_type = models.CharField(max_length=7, choices=ACCOUNT_TYPES)
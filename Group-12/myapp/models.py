from django.db import models

# Create your models here.
# Models are the way we interact with the database
class Listing(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField('date of listing')
    price = models.PositiveIntegerField()
    zipCode = models.PositiveIntegerField()
    dateAdded = models.PositiveIntegerField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class User(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    ACCOUNT_TYPES = {
        ('0', 'Buyer'),
        ('1', 'Seller'),
    }
    account_type = models.CharField(max_length=7, choices=ACCOUNT_TYPES)

    def __str__(self):
        return self.username

class Messages(models.Model):
    body = models.CharField(max_length=1000)
    senderID = models.ManyToManyField(User)
    targetID = models.CharField(max_length=25)
    date_sent = models.DateTimeField(auto_now=False, auto_now_add = True)

    def __str__(self):
        return self.body

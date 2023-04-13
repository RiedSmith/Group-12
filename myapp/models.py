from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# -*- coding: utf-8 -*-
# Create your models here.
# Models are the way we interact with the database

class Listing(models.Model):
    productName = models.CharField(max_length=200, null=True)
    productID = models.PositiveIntegerField(0)
    sellerID = models.PositiveIntegerField(0, null=True)
    listingID = models.PositiveIntegerField(0)
    #dateAdded = models.DateTimeField(auto_now=False, auto_now_add = True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desc = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.productName
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField()
    account_type_choices = [
        ('B', 'Buyer'),
        ('S', 'Seller'),
    ]
    account_type = models.CharField(max_length=10, choices=account_type_choices, null=True)
    location = models.CharField(max_length=30, null=True)
    
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Messages(models.Model):
    body = models.CharField(max_length=1000, null=True)
    senderID = models.CharField(max_length=25,null=True)
    targetID = models.CharField(max_length=25,null=True)
    date_sent = models.DateTimeField(auto_now=False, auto_now_add = True)

    def __str__(self):
        return self.body

class Watchlist(models.Model):
    Owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ManyToManyField(Listing)


class ShoppingCart(models.Model):
    listing = models.ManyToManyField(Listing)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
# -*- coding: utf-8 -*-
# Create your models here.
# Models are the way we interact with the database
 
class Listing(models.Model):
    productName = models.CharField(max_length=200, blank=' ', default = "item")
    sellerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings', default=None)
    dateAdded = models.DateTimeField(default=datetime.now, blank=' ')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desc = models.CharField(max_length=200, blank=' ', default="text")
    image = models.ImageField(upload_to='images/', null = True)

    def __str__(self):
        return self.productName
    
    def get_absolute_url(self):
        return reverse('listing_details', kwargs={'listing_id': self.id})
   

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField()
    balance = models.IntegerField(default = 0)
    account_type_choices = [
        ('B', 'Buyer'),
        ('S', 'Seller'),
    ]
    account_type = models.CharField(max_length=10, choices=account_type_choices, default="B")
    location = models.CharField(max_length=30, blank="", default="place")
    cart = models.ManyToManyField(Listing)
    
    def __str__(self):
        return self.user.username


    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Watchlist(models.Model):
    Owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ManyToManyField(Listing)

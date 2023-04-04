from django.db import models
from django.contrib.auth import get_user_model
# -*- coding: utf-8 -*-
# Create your models here.
# Models are the way we interact with the database

User = get_user_model()


class Listing(models.Model):
    productName = models.CharField(max_length=200, null=True)
    productID = models.PositiveIntegerField(0)
    sellerID = models.PositiveIntegerField(0, null=True)
    listingID = models.PositiveIntegerField(0)
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add = True)

    def __str__(self):
        return self.title
    
    


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

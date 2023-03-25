from django.db import models
# -*- coding: utf-8 -*-
# Create your models here.
# Models are the way we interact with the database
class Listing(models.Model):
    title = models.CharField(max_length=200, null=True)
    price = models.PositiveIntegerField(0)
    zipCode = models.PositiveIntegerField(0)
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add = True)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Messages(models.Model):
    body = models.CharField(max_length=1000, null=True)
    senderID = models.CharField(max_length=25,null=True)
    targetID = models.CharField(max_length=25,null=True)
    date_sent = models.DateTimeField(auto_now=False, auto_now_add = True)

    def __str__(self):
        return self.body


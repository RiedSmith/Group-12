from django.contrib import admin

# Register your models here.
from .models import Listing, ShoppingCart, Watchlist, Profile
#This is the process for registering any new models to the website
admin.site.register(Listing)
admin.site.register(Profile)
admin.site.register(Watchlist)
admin.site.register(ShoppingCart)

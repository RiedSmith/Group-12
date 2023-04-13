from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from myapp.models import Profile
from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Listing



account_type_choices = [
    ('B', 'Buyer'),
    ('S', 'Seller'),
]

class ProfileForm(UserCreationForm):
    account_type = forms.ChoiceField(
        label="Choose Account Type:",
        widget=forms.Select,
        choices=account_type_choices
    )
    email = forms.CharField(label="Email", max_length=30)
    location = forms.CharField(label="City", max_length=30)
    class Meta:
        model = User
        fields = ('username','password1', 'password2',)
        labels = {'account_type' : 'Account Type'}

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['productName', 'desc', 'price', 'image']
        widgets = {
            'image': ClearableFileInput(attrs={'multiple': False}),
        }
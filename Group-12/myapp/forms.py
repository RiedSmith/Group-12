from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

class ProfileForm(UserCreationForm):
    account_type = forms.charField(max_length = 10)
    class Meta:
        model = User
        fields = ('username', 'account_type', 'password1', 'password2',)
        labels = {'account_type' : 'Account Type'}
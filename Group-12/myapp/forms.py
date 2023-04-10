from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm


account_type_choices = [
    ('B', 'Buyer'),
    ('S', 'Seller'),
]

class ProfileForm(UserCreationForm):
    account_type = forms.MultipleChoiceField(
        label="Choose Account Type:",
        required=True,
        widget=forms.Select,
        choices=account_type_choices
    )
    email = forms.CharField(label="Email", max_length=30)
    class Meta:
        model = User
        fields = ('username', 'account_type', 'password1', 'password2',)
        labels = {'account_type' : 'Account Type'}
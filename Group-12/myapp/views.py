from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Profile, User
# Create your views here.


def home(request):
    return render(request, "main_pages/mainpage.html")

def login_view(request):
    if request.method == 'POST':
        if Profile.account_type == 'B':
            return render(request, 'main_pages/mainpage.html')
        else:
            return render(request, 'main_pages/seller_portal.html')
    return render(request, 'main_pages/mainpage.html')


def signup(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            acct_type = form.cleaned_data['account_type']
            location = form.cleaned_data['location']
            u = User(username=user)
            u.set_password(password)
            u.save()
            p = Profile(user=u, email=email, account_type=acct_type, location='location')
            p.save()
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect(reverse('login_view'))
    else:
        form = ProfileForm()
    return render(request, 'registration/signup.html', {'form': form})

    


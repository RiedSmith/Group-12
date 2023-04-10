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
    return render(request, "registration/login.html")

def signup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            acct_type = form.cleaned_data['account_type']
            email = form.cleaned_data['email']
            u = User(username = user, password = password)
            u.save()
            p = Profile(user=u, email = email, account_type = acct_type)
            p.save()

            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = ProfileForm()
    return render(request, 'registration/signup.html', {'form': form})

def account_dropdown(request):
    account_type = request.GET.get('account')
  

  
    


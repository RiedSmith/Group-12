from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.urls import revers
# Create your views here.


def home(request):
    return render(request, "main_pages/mainpage.html")

def login_view(request):
    return render(request, "registration/login.html")

def signup(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.save()
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        return()
    return render(request, 'signup.html', {'form' : form})
        


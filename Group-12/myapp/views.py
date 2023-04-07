from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.


def home(request):
    return render(request, "main_pages/mainpage.html")

def login_view(request):
    return render(request, "registration/login.html")

def signup(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
    else:
        form = ProfileForm()

    context = {
        'form' : form
    }
    render(request, 'registration/signup.html', context)

  
    


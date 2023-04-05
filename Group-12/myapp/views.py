from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.shortcuts import redirect, render
# Create your views here.


def home(request):
    return render(request, "main_pages/mainpage.html")

def login_view(request):
    return render(request, "registration/login.html")
        


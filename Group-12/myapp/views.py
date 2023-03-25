from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, "main_pages/mainpage.html")





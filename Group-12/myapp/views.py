from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.shortcuts import redirect, render
# Create your views here.


def home(request):
    return render(request, "main_pages/mainpage.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'registration/login.html', {'error_message': error_message})
    else:
        return render(request, 'registration/login.html')





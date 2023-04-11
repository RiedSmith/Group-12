from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Profile, User
from .models import Listing
# Create your views here.


def home(request):
    return render(request, "main_pages/mainpage.html")

def buyer(request):
    return render(request, "main_pages/buymainpage.html")

def seller_portal(request):
    return render(request, "main_pages/seller_portal.html")

def get_account_type(user):
    try:
        profile = Profile.objects.get(user=user)
        return profile.account_type
    except Profile.DoesNotExist:
        return None
    
def login_view(request):
    print("In login view")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        account_type = get_account_type(user)
        print("User is authenticated")
        if user is not None:
            login(request, user)
            print("User is logged in")
            if account_type == 'B':
                print("User is a buyer")
                return redirect(reverse('buyer'))
            print("User is a seller")
            return redirect(reverse('seller'))
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html')

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

@login_required
def display_user_listings(request):
    user_listings = Listing.objects.filter(sellerID=request.user.id)
    return render(request, 'user_listings.html', {'listings': user_listings})


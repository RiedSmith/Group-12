from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Profile, User
from .models import Listing
from django.contrib.auth import logout
# Create your views here.


def home(request):
    return render(request, "main_pages/mainpage.html")

def buyer(request):
    return render(request, "main_pages/buymainpage.html")

def seller_portal(request):
    return render(request, "main_pages/seller_portal.html")

def addlisting(request):
    return render(request, "main_pages/addlisting.html")

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
                return redirect(reverse('get_all_product_names'))
            print("User is a seller")
            return redirect(reverse('display_user_listings'))
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html')

def logout_view(request):    
    # remove the reference to the user object
    request.user = None
    return redirect(reverse('main_get_all_product_names'))

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
    user_listings = Listing.objects.filter(sellerID=request.user.id).values_list('productName', flat=True)
    return render(request, 'main_pages/seller_portal.html', {'product_names': user_listings})

def get_all_product_names(request):
    all_products = Listing.objects.all()
    
    return render(request, 'main_pages/buymainpage.html', {'products': all_products})

def main_get_all_product_names(request):
    all_products = Listing.objects.all()
    
    return render(request, 'main_pages/mainpage.html', {'products': all_products})

@login_required
def add_listing(request):
    if request.method == 'POST':
        # Get the form data from the request
        item_name = request.POST['item-name']
        description = request.POST['description']
        price = float(request.POST['price'])

        # Create a new listing object and set its attributes
        listing = Listing()
        listing.productName = item_name
        listing.desc = description
        listing.price = price
        listing.sellerID = request.user.profile.pk
        listing.productID = request.user.profile.pk
        listing.listingID = request.user.profile.pk

        # Save the listing to the database
        listing.save()

        # Redirect to the listing detail page
        return redirect(reverse('display_user_listings'))

    return render(request, 'listingadder/')


from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render,get_object_or_404
from .forms import ProfileForm, ListingForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Profile, User
from .models import Listing
from django.contrib.auth import logout
from django.http import JsonResponse
# Create your views here.


def home(request):
    return render(request, "main_pages/mainpage.html")

def buyer(request): #This renders the buyer profile
    return render(request, "main_pages/buymainpage.html")

def portal(request): #Context switch to change the destination of the profile button based on account type
    user = request.user
    acct_type = get_account_type(user)
    if request.user.is_authenticated:
        if acct_type == 'B':
            return render(request, "main_pages/buyer_page.html")
        else:
            return redirect(reverse('display_user_listings'))
    else:
        return redirect(reverse('login_view'))

def get_account_type(user):
    try:
        profile = Profile.objects.get(user=user)
        return profile.account_type
    except Profile.DoesNotExist:
        return None
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        account_type = get_account_type(user)
        if user is not None:
            login(request, user)
            if account_type == 'B':
                return redirect(reverse('main_get_all_product_names'))
            return redirect(reverse('display_user_listings'))
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html')

def logout_view(request):    
    logout(request)
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
    user_listings = Listing.objects.filter(sellerID=request.user)
    return render(request, 'main_pages/seller_portal.html', {'listings': user_listings})

def main_get_all_product_names(request):
    all_products = Listing.objects.all()
    return render(request, 'main_pages/mainpage.html', {'listings': all_products})

@login_required
def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(request.user)
            return redirect('display_user_listings')
        else:
            print(form.errors)
    else:
        form = ListingForm()
    return render(request, 'main_pages/addlisting.html', {'form': form})

@login_required
def delete_listing(request): #Pretty self explanatory
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        listing = Listing.objects.get(id=listing_id)
        listing.delete()
        return redirect('display_user_listings')
    return HttpResponseBadRequest("Invalid request")

def listing_details(request, listing_id): #This is what we use to display a particular listing for the details html
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'main_pages/listing_details.html', {'listing': listing})


def add_to_cart(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    user_profile = request.user.profile
    user_profile.cart.add(listing)
    return redirect('cart')

def remove_from_cart(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    user_profile = request.user.profile
    user_profile.cart.remove(listing)
    return redirect('cart')

def cart_view(request):
    user = request.user
    if user.is_authenticated:
        profile = user.profile
        listings = profile.cart.all()
        return render(request, 'main_pages/cart.html', {'listings': listings})
    else:
        return render(request, 'registration/signup.html')
    
def search_listings(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            listings = Listing.objects.filter(productName__icontains=query)
            return render(request, 'main_pages/mainpage.html', {'listings': listings})
    return redirect(reverse('main_get_all_product_names'))
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render,get_object_or_404
from .forms import ProfileForm, ListingForm, BuyerProfileForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Profile, User, Listing
from django.contrib.auth import logout
from django.http import JsonResponse
# Create your views here.


def home(request):
    return render(request, "main_pages/mainpage.html")

@login_required(login_url='/login/')
def buyer(request): #This renders the buyer profile
    response = render(request, 'main_pages/buymainpage.html')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'
    return response
    # return render(request, "main_pages/buymainpage.html")

def portal(request): #Context switch to change the destination of the profile button based on account type
    user = request.user
    acct_type = get_account_type(user)
    if request.user.is_authenticated:
        if acct_type == 'B':
            return redirect(reverse('buyer_page'))
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

@login_required(login_url='/login/')
def display_user_listings(request):
    user_listings = Listing.objects.filter(sellerID=request.user)
    response = render(request, 'main_pages/seller_portal.html', {'listings': user_listings})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'
    return response
    # return render(request, 'main_pages/seller_portal.html', {'listings': user_listings})

def main_get_all_product_names(request):
    all_products = Listing.objects.all()
    response = render(request, 'main_pages/mainpage.html', {'listings': all_products})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'
    return response
    # return render(request, 'main_pages/mainpage.html', {'listings': all_products})

@login_required(login_url='/login/')
def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(request.user)
            response = render(redirect('display_user_listings'))
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Expires'] = '0'
            return response
            # return redirect('display_user_listings')
        else:
            print(form.errors)
    else:
        form = ListingForm()
    response = render(request, 'main_pages/addlisting.html', {'form': form})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'
    return response
    # return render(request, 'main_pages/addlisting.html', {'form': form})


def delete_listing(request): #Pretty self explanatory
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        listing = Listing.objects.get(id=listing_id)
        listing.delete()
        return redirect('display_user_listings')
    return HttpResponseBadRequest("Invalid request")

login_required(login_url='/login/')
def listing_details(request, listing_id): #This is what we use to display a particular listing for the details html
    listing = get_object_or_404(Listing, pk=listing_id)
    response = render(request, 'main_pages/listing_details.html', {'listing': listing})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'
    return response
    # return render(request, 'main_pages/listing_details.html', {'listing': listing})


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

@login_required(login_url='/login/')
def cart_view(request):
    user = request.user
    if user.is_authenticated:
        profile = user.profile
        listings = profile.cart.all()
        response = render(request, 'main_pages/cart.html', {'listings': listings})
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Expires'] = '0'
        return response
        # return render(request, 'main_pages/cart.html', {'listings': listings})
    else:
        return render(request, 'registration/signup.html')
    
def search_listings(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            listings = Listing.objects.filter(productName__icontains=query)
            response = render(request, 'main_pages/mainpage.html', {'listings': listings})
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Expires'] = '0'
            return response
            # return render(request, 'main_pages/mainpage.html', {'listings': listings})
    response = render(redirect(reverse('main_get_all_product_names')))
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'
    return response
    # return redirect(reverse('main_get_all_product_names'))

@login_required(login_url='/login/')
def checkout(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse('login_view'))

    # get user's profile and cart items
    profile = user.profile
    cart_items = profile.cart.all()

    # calculate total price of cart items
    total_price = sum([item.price for item in cart_items])

    # subtract total price from buyer's balance
    if profile.balance < total_price:
        messages.error(request, 'Insufficient balance for checkout.')
        return redirect(reverse('buyer_page'))
    profile.balance -= total_price
    profile.save()

    for item in cart_items:
        # remove the item listing from the seller's account
        listing = item
        # delete the listing object
        listing.delete()

    # clear the user's cart
    profile.cart.clear()

    # display success message and redirect to main page
    messages.success(request, 'Checkout successful!')
    response = render(redirect(reverse('main_get_all_product_names')))
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'
    return response
    # return redirect(reverse('main_get_all_product_names'))


@login_required(login_url='/login/')
def add_balance(request):
    print("Hello?")
    if request.method == 'POST':
        amount = int(request.POST['balance'])
        print("Acquired the number")
        if amount <= 0:
            messages.error(request, 'Amount must be a positive integer.')
        else:
            request.user.profile.balance += amount
            print("Adding")
            request.user.profile.save()
            messages.success(request, f'Added {amount} to your balance.')
            print("This worked")
        response = render(redirect('buyer_page'))
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Expires'] = '0'
        return response
        # return redirect('buyer_page')
    else:
        print("Nice work")
        response = render(request, 'buyer_page.html')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Expires'] = '0'
        return response
        # return render(request, 'buyer_page.html')
    
@login_required(login_url='/login/')
def buyer_page(request):
    if request.method == 'POST':
        print("request")
        if 'balance' in request.POST:
            amount = request.POST.get('balance')
            user_profile = request.user.profile
            print("user profile is new")
            user_profile.balance += int(amount)
            print("balance saved")
            user_profile.save()
            messages.success(request, f'Balance updated successfully')
            return redirect('buyer_page')

        form = BuyerProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            print("Form is valid")
            form.save()
            messages.success(request, f'Profile updated successfully')
            return redirect('buyer_page')
    else:
        form = BuyerProfileForm(instance=request.user.profile)
    return render(request, 'main_pages/buyer_page.html', {'form': form})
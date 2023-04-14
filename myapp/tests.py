#forms.py test case:
from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from myapp.forms import ProfileForm
from .models import *

# Create your tests here.
class ProfileFormTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'account_type': 'B',
            'email': 'testuser@example.com',
            'location': 'New York',
        }

    def test_valid_form(self):
        form = ProfileForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        required_fields = ['username', 'password1', 'password2', 'account_type', 'email', 'location']
        form = ProfileForm()
        for field in required_fields:
            self.assertTrue(form.fields[field].required)

    def test_username_field(self):
        # Test that username field has correct max length
        form = ProfileForm()
        self.assertEqual(form.fields['username'].max_length, 150)

        # Test that username field is unique
        User.objects.create_user(username='testuser', password='testpassword123')
        form = ProfileForm(data=self.user_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_email_field(self):
        # Test that email field has correct max length
        form = ProfileForm()
        self.assertEqual(form.fields['email'].max_length, 30)

        # Test that email field is required
        self.assertTrue(form.fields['email'].required)

        # Test that email field accepts valid emails
        self.user_data['email'] = 'testuser@example.com'
        form = ProfileForm(data=self.user_data)
        self.assertTrue(form.is_valid())

        # Test that email field rejects invalid emails
        self.user_data['email'] = 'invalidemail'
        form = ProfileForm(data=self.user_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_location_field(self):
        # Test that location field has correct max length
        form = ProfileForm()
        self.assertEqual(form.fields['location'].max_length, 30)

        # Test that location field is required
        self.assertTrue(form.fields['location'].required)

    def test_account_type_field(self):
        # Test that account type field is required
        form = ProfileForm()
        self.assertTrue(form.fields['account_type'].required)

        # Test that account type field accepts valid choices
        self.user_data['account_type'] = 'B'
        form = ProfileForm(data=self.user_data)
        self.assertTrue(form.is_valid())

        # Test that account type field rejects invalid choices
        self.user_data['account_type'] = 'invalid_choice'
        form = ProfileForm(data=self.user_data)
        self.assertFalse(form.is_valid())
        self.assertIn('account_type', form.errors)


#Profile model test and listing test
class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@test.com', password='testpass')
        self.profile = Profile.objects.create(
            user=self.user, email='test@test.com', account_type='Buyer', location='New York')

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.email, 'test@test.com')
        self.assertEqual(self.profile.account_type, 'Buyer')
        self.assertEqual(self.profile.location, 'New York')

class ListingModelTest(TestCase):
    def setUp(self):
        self.listing = Listing.objects.create(
            productName='iPhone 13', productID=12345, sellerID=54321, listingID=1)

    def test_listing_creation(self):
        self.assertEqual(self.listing.productName, 'iPhone 13')
        self.assertEqual(self.listing.productID, 12345)
        self.assertEqual(self.listing.sellerID, 54321)
        self.assertEqual(self.listing.listingID, 1)

#Test Case: Create a Listing object
from .models import Listing

class ListingTestCase(TestCase):
    def setUp(self):
        Listing.objects.create(productName="Test Product", productID=1234, sellerID=5678, listingID=9012)
    
    def test_listing_creation(self):
        product = Listing.objects.get(productName="Test Product")
        self.assertEqual(product.productID, 1234)
        self.assertEqual(product.sellerID, 5678)
        self.assertEqual(product.listingID, 9012)

#Test Case: Add a Listing object to a user's watchlist
from .models import Listing, Watchlist

class WatchlistTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="testuser@test.com", password="testpassword")
        listing = Listing.objects.create(productName="Test Product", productID=1234, sellerID=5678, listingID=9012)
        watchlist = Watchlist.objects.create(Owner=user)
        watchlist.item.add(listing)
    
    def test_watchlist_addition(self):
        user = User.objects.get(username="testuser")
        watchlist = Watchlist.objects.get(Owner=user)
        self.assertEqual(watchlist.item.count(), 1)
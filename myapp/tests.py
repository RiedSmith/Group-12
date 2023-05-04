
from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from myapp.forms import ProfileForm
from .models import *
from .models import Listing, Watchlist
from datetime import datetime
from myapp.models import Listing, User
from myapp.forms import ListingForm
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.
class AddListingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_add_listing_post_request(self):
        data = {
            'title': 'Test Listing',
            'description': 'This is a test listing',
            'price': 10.99,
            'image': SimpleUploadedFile('test_image.jpg', b'test data'),
        }
        form = ListingForm(data)
        response = self.client.post('/add_listing/', data, follow=True)

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

class ListingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='seller1', password='password')
        self.listing = Listing.objects.create(
            productName='iPhone 13', 
            sellerID=self.user, 
            dateAdded=datetime.now(), 
            price=1200.00,
            desc='Brand new iPhone 13',
            image=None
        )

    def test_listing_creation(self):
        self.assertEqual(self.listing.productName, 'iPhone 13')
        self.assertEqual(self.listing.sellerID, self.user)
        self.assertIsNotNone(self.listing.dateAdded)
        self.assertEqual(self.listing.price, 1200.00)
        self.assertEqual(self.listing.desc, 'Brand new iPhone 13')

    def test_listing_str(self):
        self.assertEqual(str(self.listing), 'iPhone 13')



class WatchlistTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="testuser@test.com", password="testpassword")
        listing = Listing.objects.create(productName="Test Product", productID=1234, sellerID=5678, listingID=9012)
        watchlist = Watchlist.objects.create(Owner=user)
        watchlist.item.add(listing)
    
class ProfileFormTests(TestCase): 
    def test_valid_form(self): 
        form = ProfileForm({ 'username': 'testuser', 'email': 'test@test.com', 'password1': 'testpass', 'password2': 'testpass', 'account_type': 'B', 'location': 'New York' })

    def test_missing_required_field(self):
        form = ProfileForm({
            'username': 'testuser',
            'email': '',
            'password1': 'testpass',
            'password2': 'testpass',
            'account_type': 'B',
            'location': 'New York'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This field is required.'])

    def test_invalid_email_format(self):
        form = ProfileForm({
            'username': 'testuser',
            'email': 'test',
            'password1': 'testpass',
            'password2': 'testpass',
            'account_type': 'B',
            'location': 'New York'
        })
        self.assertFalse(form.is_valid())

    def test_passwords_do_not_match(self):
        form = ProfileForm({
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpass',
            'password2': 'wrongpass',
            'account_type': 'B',
            'location': 'New York'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])

    def test_invalid_account_type_choice(self):
        form = ProfileForm({
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpass',
            'password2': 'testpass',
            'account_type': 'X',
            'location': 'New York'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['account_type'], ['Select a valid choice. X is not one of the available choices.'])

    class WatchlistTestCase(TestCase): 
        def setUp(self): 
            self.user1 = User.objects.create_user(username="user1", email="user1@test.com", password="password123") 
            self.user2 = User.objects.create_user(username="user2", email="user2@test.com", password="password123") 
            self.listing1 = Listing.objects.create(productName="Product1", sellerID=self.user1, price=50.00) 
            self.listing2 = Listing.objects.create(productName="Product2", sellerID=self.user1, price=100.00) 
            self.listing3 = Listing.objects.create(productName="Product3", sellerID=self.user2, price=75.00) 
            self.watchlist1 = Watchlist.objects.create(Owner=self.user1) 
            self.watchlist2 = Watchlist.objects.create(Owner=self.user2)

        def test_watchlist_creation(self):
            self.assertEqual(self.watchlist1.Owner.username, "user1")
            self.assertEqual(self.watchlist2.Owner.username, "user2")

        def test_watchlist_add_listing(self):
            self.watchlist1.item.add(self.listing1)
            self.watchlist1.item.add(self.listing2)
            self.assertEqual(self.watchlist1.item.count(), 2)
            self.assertEqual(self.watchlist2.item.count(), 0)
            self.watchlist2.item.add(self.listing3)
            self.assertEqual(self.watchlist2.item.count(), 1)
            self.assertEqual(self.watchlist2.item.first().productName, "Product3")

class ListingFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'productName': 'Product Test',
            'desc': 'This is a test description',
            'price': 100,
        }
        form = ListingForm(data=form_data)
        
    def test_invalid_form(self):
        form_data = {
            'productName': '',
            'desc': 'This is a test description',
            'price': 0,
        }
        form = ListingForm(data=form_data)
        self.assertFalse(form.is_valid())

class ListingFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
    

    
    def test_form_required_fields(self):
        data = {}
        form = ListingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors.keys())

    def test_form_non_numeric_fields(self):
        data = {
            'productName': 'Test Product',
            'desc': 'This is a test product',
            'price': 'not a number',
            'image': SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            'quantity': 'not a number'
        }
        form = ListingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors.keys())
        self.assertIn('quantity', form.errors.keys())
    
    def test_form_invalid_image_file(self):
        data = {
            'productName': 'Test Product',
            'desc': 'This is a test product',
            'price': 10.00,
            'image': SimpleUploadedFile("test.txt", b"file_content", content_type="text/plain"),
            'quantity': 5
        }
        form = ListingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors.keys())

    def test_form_invalid_image_file_type(self):
        form_data = {
            'productName': 'Test Product',
            'desc': 'This is a test product',
            'price': 10.00,
            'image': SimpleUploadedFile("test_file.txt", b"file_content", content_type="text/plain"),
            'quantity': 5
        }
        form = ListingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('image' in form.errors)
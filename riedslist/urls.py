"""riedslist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView, View
from myapp import views as user_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home/', TemplateView.as_view(template_name='main_pages/mainpage.html'), name='home'),
    path('', user_view.main_get_all_product_names, name='main_get_all_product_names'),
    path('admin/', admin.site.urls),
    path('account/', include("django.contrib.auth.urls")),
    path('login/', user_view.login_view, name='login_view'),
    path('signup/', user_view.signup, name='signup' ),
    path('wishlist/', TemplateView.as_view(template_name='main_pages/wishlist.html'), name='wishlist'),
    path('portal/', user_view.portal, name='portal'),
    path('logout/', user_view.logout_view, name='logout_view'),
    path('addlisting/', user_view.add_listing, name='addlisting'),
    path('displaylisting/', user_view.display_user_listings, name='display_user_listings'),
    path('deletelistings/', user_view.delete_listing,name='delete_listing'),
    path('add_to_cart/<int:listing_id>/', user_view.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:listing_id>/', user_view.remove_from_cart, name='remove_from_cart'),
    #path('displayall/', user_view.get_all_product_names, name='get_all_product_names'),
    path('listings/<int:listing_id>/', user_view.listing_details, name='listing_details'),
    path('cart/', user_view.cart_view, name = 'cart'),
    path('search/', user_view.search_listings, name='search_listings'),
    path('checkout/', user_view.checkout, name='checkout'),
    path('add_balance/', user_view.add_balance, name='add_balance'),
    path('buyer_page/', user_view.buyer_page, name='buyer_page')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

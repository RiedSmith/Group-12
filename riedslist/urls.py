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


urlpatterns = [
    path('', TemplateView.as_view(template_name='main_pages/mainpage.html'), name='home'),
    path('admin/', admin.site.urls),
    path('account/', include("django.contrib.auth.urls")),
    path('login/', user_view.login_view, name='login_view'),
    path('signup/', user_view.signup, name='signup' ),
    path('buyer/', TemplateView.as_view(template_name='main_pages/buymainpage.html'), name='buyer'),
    path('wishlist/', TemplateView.as_view(template_name='main_pages/wishlist.html'), name='wishlist'),
    path('seller/', TemplateView.as_view(template_name='main_pages/seller_portal.html'), name='seller'),
    path('logout/', user_view.logout_view, name='logout_view'),
    path('add_listing/', user_view.add_listing, name='add_listing'),
    path('seller/listingadder/', TemplateView.as_view(template_name='main_pages/addlisting.html'), name='addlisting'),
    path('displaylisting/', user_view.display_user_listings, name='display_user_listings'),
    path('displayall/', user_view.get_all_product_names, name='get_all_product_names'),
]


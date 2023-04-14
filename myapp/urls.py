from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView, View
from myapp import views as user_view
from . import views

urlpatterns = [
    path('', views.main_get_all_product_names, name='get_stuff'),
    path('admin/', admin.site.urls),
    path('account/', include("django.contrib.auth.urls")),
    path('login/', user_view.login_view, name='login_view'),
    path('signup/', user_view.signup, name='signup' ),
    path('buyer/', TemplateView.as_view(template_name='main_pages/buymainpage.html'), name='buyer'),
    path('wishlist/', TemplateView.as_view(template_name='main_pages/wishlist.html'), name='wishlist'),
    path('seller/', TemplateView.as_view(template_name='main_pages/seller_portal.html'), name='seller'),
    path('logout/', user_view.logout_view, name='logout_view'),
    #path('addlisting/', user_view.add_listing, name='addlisting'),
    path('displaylisting/', user_view.display_user_listings, name='display_user_listings'),
]


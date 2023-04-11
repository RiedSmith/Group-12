from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView, View
from myapp import views as user_view
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='main_pages/mainpage.html'), name='home'),
    path('admin/', admin.site.urls),
    path('account/', include("django.contrib.auth.urls")),
    path('login/', views.login_view, name='login_view'),
    path('signup/', user_view.signup, name='signup' ),
    path('buyer/', TemplateView.as_view(template_name='main_pages/buymainpage.html'), name='buyer'),
    path('seller/', TemplateView.as_view(template_name='main_pages/seller_portal.html'), name='seller_portal'),
]


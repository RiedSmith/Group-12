from django.urls import path, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

# URLConf
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
]

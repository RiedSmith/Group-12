from django.urls import path, include
from . import views as user_view
from django.contrib import admin
from django.contrib.auth import views as auth_views

# URLConf
urlpatterns = [
    path('', user_view.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', user_view.signup, name='signup'),
]

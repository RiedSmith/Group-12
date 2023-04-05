from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home')
]

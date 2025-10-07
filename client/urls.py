from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/signup', views.signup, name='signup'),
    path('auth/login', views.login, name='login'),
]

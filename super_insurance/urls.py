from django.contrib import admin
from django.urls import path, include

from client import views
from users import views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', admin.site.urls),
    path('client/', include('client.urls')),
    path('users/', include('users.urls')),
    path('company/', include('company.urls')),
]

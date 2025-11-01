from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from client import views
from users import views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', views.home, name="home"),
    path('client/', include('client.urls')),
    path('users/', include('users.urls')),
    path('company/', include('company.urls')),
)

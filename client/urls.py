from django.urls import path
from . import views

app_name = "client"

urlpatterns = [
    path('', views.home, name='home'),
    path('solicitation/', views.create_solicitation, name='create_solicitation'),
]

from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    path('', views.home, name='home'),
    path('solicitations/', views.solicitations, name='solicitations'),
    path('create-user/', views.create_user_with_policy, name='create_user_with_policy'),
]

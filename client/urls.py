from django.urls import path
from . import views

app_name = "client"

urlpatterns = [
    path('', views.home, name='home'),
    path('solicitation/', views.create_solicitation, name='create_solicitation'),
    path('solicitations/', views.solicitations, name='solicitations'),
    path('solicitations/<int:solicitation_id>/', views.solicitation_details, name='solicitation_details'),
]

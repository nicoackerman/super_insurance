from django.urls import path
from . import views

app_name = "company"

urlpatterns = [
    path('home/', views.home, name="home"),
    path('solicitations/', views.solicitations, name="solicitations"),
    path('create-user-with-policy/', views.create_user_with_policy, name="create_user_with_policy"),
    path('create-policy/', views.create_policy, name="create_policy"),
    path('policies/', views.policies, name="policies"),
    path('edit/<int:policy_id>/', views.edit_policy, name="edit_policy"),
    path('delete/<int:policy_id>/', views.delete_policy, name="delete_policy"),
    path('users/', views.user_list, name="user_list"),
    path('users/<int:user_id>/add-policy/', views.add_policy_to_user, name='add_policy_to_user'),
    path('users/edit-policy/<int:user_policy_id>/', views.edit_user_policy, name='edit_user_policy'),
    path('policies/<int:policy_id>/details/', views.policy_details, name='policy_details'),
]

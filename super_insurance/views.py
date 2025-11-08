from django.shortcuts import render, redirect
from django.urls import reverse

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(reverse('company:home'))
        else:
            return redirect(reverse('client:home'))
    return render(request, 'home_app.html')

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def login(request):
    return render(request, 'users/login.html')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("client:home")
    else:
        form = UserCreationForm()
    
    return render(request, 'users/signup.html', {"form": form})

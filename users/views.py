from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, logout

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")

def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("home")
        else:
            print(form.errors)
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {"form": form})

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("client:home")
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/signup.html', {"form": form})

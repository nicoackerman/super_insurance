from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("home")
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {"form": form})

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("client:home")
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    
    return render(request, 'users/signup.html', {"form": form})

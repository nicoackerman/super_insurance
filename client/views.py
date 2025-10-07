from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'client/home.html')

def login(request):
    return render(request, 'client/login.html')

def signup(request):
    return render(request, 'client/signup.html')

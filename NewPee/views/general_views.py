from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.

def header(request, format=None):
    return render(request, 'header.html', {})
  
def home(request, format=None):
    return render(request, 'homepage.html', {})

def log_in(request, format=None):
    return render(request, 'login.html', {})

def sign_up(request, format=None):
    return render(request, 'signup.html', {})
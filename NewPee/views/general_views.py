from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.

def header(request, format=None):
    return render(request, 'header.html', {})
  
def homepage(request, format=None):
    return render(request, 'homepage.html', {})
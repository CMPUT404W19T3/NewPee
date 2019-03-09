from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.
def header(request):
    return render(request, 'header.html', {})

def homepage(request):
    return render(request, 'homepage.html', {})
from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.
def log_in(request):
    return render(request, 'login.html', {})

def sign_up(request):
    return render(request, 'signup.html', {})

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .forms import UserNameForm, UserLoginForm, postTitleForm, postInfoForm, passwordLoginForm
from Authors.models import Author
from django.contrib.auth.models import User
from Posts.models import Post
from django.contrib.auth import authenticate, login
import json

from rest_framework import status
#from rest_framework import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.

# The post is now created.
# TODO : May need some work? on handling the body content.

def logout_view(request):
    logout(request)
    return redirect('/login')

def log_in(request, format=None):

        if request.method == 'POST':

            form = UserLoginForm(request.POST)

            if form.is_valid():

                print("Form is valid:")

                #form.save()

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = authenticate(request, username=username, password=password)

                if user is not None:

                    login(request, user)

                    return HttpResponseRedirect('../authors/', {'form': form})

                return render(request, 'login.html', {'form': form})

            else:
                
                return render(request, 'login.html', {})

        else:

            form = UserLoginForm()

            return render(request, 'registration/login.html', {'form': form})


def get_author(request, format=None):


        print(request)

        pariedAuthor = Author.objects.get(user = request.user)
        author_id = pariedAuthor.get_author_id()
        
        print(author_id)

        return HttpResponseRedirect("/authors/" + str(pariedAuthor.get_author_id()))

def sign_up(request, format=None):

    if request.method == 'POST':

        # form = UserNameForm(request.POST)
        # form2 = passwordLoginForm(request.POST)

        #username = request.POST.get('username')
        #password = request.POST.get('password')

        #print("Username and password accept.")
        #print(username, password)

        # views/forms/form

        form = UserNameForm(request.POST)

        print(form)

        if form.is_valid():

            print("Form is valid:")

            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            raw_confirm_password = form.cleaned_data.get('password2')

            print(username, raw_password)

            if raw_password == raw_confirm_password:

                temp_user = authenticate(username=username, password=raw_password)

                print(temp_user)
                login(request,temp_user)

                temp_user.email = "fake@gmail.com"
                new_user = Author.objects.create(user=temp_user, displayName=temp_user.username)

                print("Account was created.")

        
                return HttpResponseRedirect("/",)

        return render(request, 'signup.html', {'form': form})

    else:

        form = UserNameForm()
        #form2 = passwordLoginForm()

        return render(request, 'signup.html', {'form': form})

def custom_login(request):
    print(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        return login(request)
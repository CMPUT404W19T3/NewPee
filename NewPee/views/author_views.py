from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .forms import UserNameForm, UserLoginForm, postTitleForm, postInfoForm, passwordLoginForm, SearchForm
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


                #form.save()

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('../authors/', {'form': form})
                

                return render(request, 'registration/login.html', {'form': form}, status=401)

            else:
                return render(request, 'registration/login.html', {})

        else:

            form = UserLoginForm()

            return render(request, 'registration/login.html', {'form': form})



def redirect(request, format=None):

    try:
        if (not request.user.is_anonymous):
            return HttpResponseRedirect("/authors/")
        else:
            return HttpResponseRedirect("/login/")
    except:
        return HttpResponseRedirect("/login/")



def get_author(request, format=None):

        print(request)

        pariedAuthor = Author.objects.get(user = request.user)
        author_id = pariedAuthor.get_author_id()
        
        print(author_id)

        return HttpResponseRedirect("/authors/" + str(pariedAuthor.get_author_id()))

def get_authors(request, format=None):

    form = SearchForm()
    print(form)
    return render(request, 'search.html/', {'form': form})

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


        if form.is_valid():


            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            raw_confirm_password = form.cleaned_data.get('password2')


            if raw_password == raw_confirm_password:

                temp_user = authenticate(username=username, password=raw_password)

                login(request,temp_user)

                temp_user.email = "fake@gmail.com"
                new_user = Author.objects.create(user=temp_user, displayName=temp_user.username)


        
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
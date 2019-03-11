from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .forms import UserNameForm, postTitleForm, postInfoForm, userLoginForm, passwordLoginForm
from Authors.models import Author
from django.contrib.auth.models import User
from Posts.models import Post
from django.contrib.auth import authenticate, login
import json

from rest_framework import status
#from rest_framework import api_view
from rest_framework.response import Response 
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


# The post is now created. 
# TODO : May need some work? on handling the body content. 

@csrf_exempt
def create_post(request, format=None):


        print(request.user)
        

        if request.method == 'POST':

            title = None;
            info = None;

            body_unicode = request.body.decode('utf-8')

            values = body_unicode.split("&")


            # Convert the body into useable info. 

            title = values[0].split('=')[1]
            title = title.split('+')

            final_title = ""
            for item in title:
                final_title = final_title + item + " "

            content = values[1].split('=')[1]
            content =  content.split('+')

            final_content = ""
            for item in  content:
                final_content =  final_content + item + " "


            print(final_content)


            description = values[2].split('=')[1]
            description =  description.split('+')

            final_description = ""
            for item in  description:
                final_description =  final_description + item + " "


            print(final_description)





            #form_title = postTitleForm(request.POST)
            #form_info = postInfoForm(request.POST)


            if (title != None and description != None):

                new_post = Post.objects.create(title= title, author = "Temp_author", description = description, content = content)
                print(" A new post was created.")






            return HttpResponse("?")






def log_in(request, format=None):


        if request.method == 'POST':

            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)

                return HttpResponseRedirect('/')



            return HttpResponse("didn't work")
        else:

            return render(request, 'login.html', {})


def sign_up(request, format=None):



    if request.method == 'POST':

        form = UserNameForm(request.POST)
        form2 = passwordLoginForm(request.POST)


        if form.is_valid() and form2.is_valid():

            username = form.cleaned_data['username']
            password = form2.cleaned_data['password']

            temp_user = User.objects.create_user(username, "fake@gmail.com", password)

            new_user = Author.objects.create(user=temp_user)



            return HttpResponseRedirect('/')
            #return HttpResponseRedirect('/thanks/')
    else:

        form = UserNameForm()
        form2 = passwordLoginForm()

        return render(request, 'signup.html', {'form': form})

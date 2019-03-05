from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .forms import UserNameForm, postTitleForm, postInfoForm, userLoginForm, passwordLoginForm
from Authors.models import Author
from django.contrib.auth.models import User
from Posts.models import Post
from django.contrib.auth import authenticate, login

# Create your views here.

def create_post(request):


        if request.method == 'POST':

            form_title = postTitleForm(request.POST)
            form_info = postInfoForm(request.POST)


            if form_title.is_valid() and form_info.is_valid():


                title = form_title.cleaned_data['post_title']
                info = form_info.cleaned_data['post_info']


                new_post = Post.objects.create(title= title, author = "Temp_author", body = info)






                return HttpResponse(new_post)
                #return HttpResponseRedirect('/thanks/')
        else:

            form_title = postTitleForm()
            form_info = postInfoForm()




        return render(request, 'create_post.html', {'form_title': form_title, 'form_info': form_info})

def log_in(request):


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


def sign_up(request):



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

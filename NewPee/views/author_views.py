from Authors.models import Author
from Authors.serializers import AuthorSerializer
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from Posts.models import Post
from Posts.serializers import PostSerializer
from rest_framework import status
from rest_framework.response import Response
from .api_views import post_list
from .forms import UserCreateForm, UserLoginForm, PostTitleForm, PostInfoForm, PasswordLoginForm, SearchForm

import json

# Create your views here.
# The post is now created.
# TODO : May need some work? on handling the body content.

def check_auth(request):

    if request.user.is_authenticated:
        return redirect(reverse('get_author'))
    else:
        return redirect(reverse('login'))

def logout_view(request):

    logout(request)

    return redirect(reverse('login'))

def api_logout(request):

    logout(request)

    return redirect(reverse('docs'))

def api_login(request):

    form = UserLoginForm(request.POST or None)

    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            author = Author.objects.get(user=user)
            if (author.isAuthorized):
                login(request, user)
                return redirect(reverse('docs'))
    return render(request, 'registration/login.html', {'form': form})

def log_in(request, format=None):

    form = UserLoginForm(request.POST or None)

    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            author = Author.objects.get(user=user)
            if (author.isAuthorized):
                login(request, user)
                return HttpResponseRedirect(reverse('get_author'), {'form': form})
    return render(request, 'registration/login.html', {'form': form})

        # if request.method == 'POST':

        #     form = UserLoginForm(request.POST)

        #     if form.is_valid():

        #         #form.save()

        #         username = form.cleaned_data.get('username')
        #         password = form.cleaned_data.get('password')

        #         user = authenticate(username=username, password=password)

        #         if user is not None:

        #             author = Author.objects.get(user=user)

        #             if (author.isAuthorized):

        #                 login(request, user)

        #                 return HttpResponseRedirect(reverse('get_author'), {'form': form})

        #             else:

        #                 return render(request, 'registration/login.html',{'form': form, 'approved': author.isAuthorized})

        #         return render(request, 'registration/login.html', {'form': form}, status=401)

        #     else:

        #         return render(request, 'registration/login.html', {'form': form})

        # # Not a POST?
        # else:

        #     form = UserLoginForm()

        #     return render(request, 'registration/login.html', {'form': form})

# def redirect(request, format=None):

#     try:

#         if (not request.user.is_anonymous):

#             return HttpResponseRedirect("/authors/")

#         else:

#             return HttpResponseRedirect("/login/")
#     except:

#         return HttpResponseRedirect("/login/")

def feed(request, format=None):

    response = post_list(request)
    
    author = Author.objects.get(user=request.user)
    serializer =  AuthorSerializer(author, context={'request': request})
    followers = author.get_followers()
    following = author.get_following()

    print(len(following))

    form = SearchForm()
    search = request.GET.get('search')

    if search:

        exclude_author = Author.objects.filter(user = request.user)
        authors = Author.objects.filter(displayName__icontains = search).exclude(pk__in=exclude_author)

        return render(request, 'search.html', {'logged_in_author': serializer.data, 'authors': authors, 'form': form, 'search': search})

    print(response.data)

    #serializer = PostSerializer(response.data,many=True,context={'request': request})
    response_list = list(response.data)
    response_list.sort(key=lambda x: x['post_date'], reverse=True)
    paginator = Paginator(response_list, 5)
    page = request.GET.get('page')
    pages = paginator.get_page(page)

    return render(request, 'feed.html', {'posts':response.data, 'logged_in_author': serializer.data, 'form': form, 'pages': pages, 'following':following, 'followers': followers})

def respond_to_friends(request, format = None):

    authors = Author.objects.all()
    current_author = Author.objects.get(user = request.user)
    friends_requests = current_author.get_friend_requests()
    declinedrequest = current_author.get_declined_requests()
    friends = current_author.friends.all()

    print(declinedrequest, "declinedrequest")
    print(friends_requests, "my friend requests")
    print(friends, "my friends")


    for friend in declinedrequest:

        friends_requests = friends_requests.exclude(id = friend.id)

    serializer_current = AuthorSerializer(current_author, context={'request': request})
    form = SearchForm()
    search = request.GET.get('search')

    if search:

        exclude_author = Author.objects.filter(user = request.user)
        authors = Author.objects.filter(displayName__icontains = search).exclude(pk__in=exclude_author)

        return render(request, 'search.html', {'logged_in_author': serializer_current.data, 'authors': authors, 'form': form, 'search': search})

    print(friends_requests, "xxxx")

    serializer_friends = AuthorSerializer(friends_requests, many=True, context={'request': request})



    return render(request, 'friends.html', { 'authors':serializer_friends.data , 'form': form, 'logged_in_author': serializer_current.data, 'friends':friends,  })

def get_author(request, format=None):

        print(request, "?")

        pariedAuthor = Author.objects.get(user = request.user)
        author_id = pariedAuthor.get_author_id()

        print(author_id, "?")

        return HttpResponseRedirect("/authors/" + str(pariedAuthor.get_author_id()))

def get_authors(request, format=None):

    form = SearchForm()

    print(form)

    return render(request, 'search.html/', {'form': form})

def sign_up(request, format=None):

    form = UserCreateForm(request.POST or None)

    if request.POST and form.is_valid():
        form.save()
        new_user = form.signup()
        Author.objects.create(user=new_user, displayName=new_user.username)
        return HttpResponseRedirect(reverse('login'), {'form': form})
    return render(request, 'signup.html', {'form': form})

    # if request.method == 'POST':

    #     # form = UserCreateForm(request.POST)
    #     # form2 = passwordLoginForm(request.POST)

    #     #username = request.POST.get('username')
    #     #password = request.POST.get('password')

    #     #print("Username and password accept.")
    #     #print(username, password)

    #     # views/forms/form

    #     form = UserCreateForm(request.POST)

        # if form.is_valid():

            # form.save()

            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # raw_confirm_password = form.cleaned_data.get('password2')

            # if raw_password == raw_confirm_password:

                # temp_user = authenticate(username=username, password=raw_password)

                # # temp_user.email = "fake@gmail.com"
                # Author.objects.create(user=temp_user, displayName=temp_user.username)

                # return HttpResponseRedirect("../login",)

        # return render(request, 'signup.html', {'form': form})

    # else:

    #     form = UserCreateForm()
    #     #form2 = passwordLoginForm()

    #     return render(request, 'signup.html', {'form': form})

def custom_login(request):

    print(request)

    if request.user.is_authenticated():

        return HttpResponseRedirect("/")

    else:

        return login(request)

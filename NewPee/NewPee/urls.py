"""NewPee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from views.author_views import log_in, sign_up, logout_view, get_author, get_authors,redirect   
from views import api_views

from Authors.views import AuthorList, AuthorDetail, AuthorfriendsView, AuthorIsfriendsView, AuthorFriendRequestsView, AuthorFriendRequestActionsView
#import Author.views
from Posts.views import PostList, PostDetail

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.documentation import include_docs_urls
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from rest_framework_swagger.views import get_swagger_view

API_TITLE = "API Documentation"
API_DESCRIPTION = 'Built-in interactive API documentation for NewPee.'

schema_view = get_swagger_view(title='Documentation')

from rest_framework import routers

urlpatterns = [
    # Login, Signup and Logout
    # path('',log_in), Root should be home if user is logged in
    #path('login/', log_in),
    url( r'^login/$', log_in, name="login"),
    path('signup/', sign_up),

    path('', redirect),
    # Admin
    path('admin/', admin.site.urls),

    # Author API
    path('api/authors/', api_views.Author_list),
    path('api/authors/<uuid:pk>', api_views.Author_detail),

    # Post API
    path('api/posts/', api_views.post_list),
    path('api/posts/<uuid:pk>', api_views.post_detail, name="edit_author"),

    #TODO
    # http://service/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID} visible to the currently authenticated user)


    #TODO 
    # http://service/posts/{post_id}/comments access to the comments in a post


    path('friends/<uuid:pk>', AuthorDetail.as_view()),

    # Search 
    path('search/', get_authors, name="search"),

    # Posts API
    # path('api/posts/', PostList.as_view()),
    # path('api/posts/<uuid:pk>', PostDetail.as_view()),

    # Author page
    path('authors/<uuid:pk>', AuthorDetail.as_view(), name="author_page"),

    # Post Modal View
    path('posts/<uuid:pk>', PostDetail.as_view(), name="post_page"),

    # Comment API
    path('api/comments/', api_views.comment_list),

    # Home
    path('home/', AuthorList.as_view(), name="home"),
    path('logout/', logout_view, name="logout"),

    path('authors/', get_author),

    # FRIENDS
    path('api/author/<uuid:pk>/friends/', AuthorfriendsView.as_view(), name="api-friendlist"),      # GET Return query of friends, # POST a list of authors, returns 
    path('api/author/<uuid:pk>/friends/<uuid:pk2>', AuthorIsfriendsView.as_view(), name="api-checkfriends"), # returns a boolean if they are friends
    path('api/author/<uuid:pk>/friendrequest/' , AuthorFriendRequestsView.as_view(), name="api-friendrequests"),

    # Friend actions
    path('api/author/<uuid:pk>/accept-friend-request/', AuthorFriendRequestActionsView.as_view(), {'method': "accept"}, name="accept-friend", ),
    path('api/author/<uuid:pk>/decline-friend-request/', AuthorFriendRequestActionsView.as_view(),{'method': "decline"}, name="decline-friend", ),
    path('api/author/<uuid:pk>/send-friend-request/', AuthorFriendRequestActionsView.as_view(), {'method': "send-request"}, name="send-request", ),
    path('api/author/<uuid:pk/unfriend/', AuthorFriendRequestActionsView.as_view(),{'method': "unfriend"}, name="unfriend",  ),

    url(r'^docs/', schema_view)
]

# https://www.django-rest-framework.org/topics/documenting-your-api/
# https://docs.djangoproject.com/en/2.1/topics/http/urls/
# https://www.django-rest-framework.org/api-guide/format-suffixes/

#urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
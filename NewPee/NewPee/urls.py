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

from Authors.views import AuthorList, AuthorDetail, AuthorfriendsView, AuthorIsfriendsView, AuthorFriendRequestsView, AuthorFriendRequestActionsView, AuthorUpdateFriendRequestsView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from Posts.views import PostList, PostDetail
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from rest_framework.urlpatterns import format_suffix_patterns
from views import api_views
from views.author_views import api_login, api_logout, check_auth, log_in, sign_up, logout_view, get_author, get_authors,redirect, feed, respond_to_friends

# https://www.django-rest-framework.org/topics/documenting-your-api/
# https://docs.djangoproject.com/en/2.1/topics/http/urls/
# https://www.django-rest-framework.org/api-guide/format-suffixes/

schema_url_patterns = [
    path('api/authors', api_views.Author_list, name="api-author"),
    path('api/authors/<uuid:pk>', api_views.Author_detail, name="api-author"),

    path('api/posts', api_views.post_list),
    path('api/posts/<uuid:pk>', api_views.post_detail, name="edit_author"),
    path('api/comments', api_views.comment_list),
    path('api/image/', api_views.image_detail),

    path('friends/<uuid:pk>', AuthorDetail.as_view()),

    path('api/friendrequest', AuthorUpdateFriendRequestsView.as_view(), name = "api-friendrequest"),
    path('api/author/<uuid:pk>/friends/', AuthorfriendsView.as_view(), name="api-friendlist"),      
    path('api/author/<uuid:pk>/friends/<uuid:pk2>', AuthorIsfriendsView.as_view(), name="api-checkfriends"), 
    path('api/author/<uuid:pk>/friendrequest' , AuthorFriendRequestsView.as_view(), name="api-returnfriendrequests"), 
    path('api/author/<uuid:pk>/decline-friend-request', AuthorFriendRequestActionsView.as_view(),{'method': "decline"}, name="decline-friend", ),
]

schema_view = get_swagger_view(
    title='NewPee API Documentation',
    patterns=schema_url_patterns
)

urlpatterns = [

    # Root will redirect to home if user is logged in
    # Otherwise it will redirect to login page
    path('', check_auth, name="check_auth"),
    path('login/', log_in, name="login"),
    path('api_login/', api_login, name="api_login"),
    path('signup/', sign_up, name="sign_up"),
    path('feed/', feed, name="feed"),

    # Admin
    path('admin/', admin.site.urls, name="admin"),

    # Author API
    path('api/authors', api_views.Author_list, name="api-author"),
    path('api/authors/<uuid:pk>', api_views.Author_detail, name="api-author"),

    # Post API
    path('api/posts', api_views.post_list),
    path('api/author/posts', api_views.post_list),  # for different groups

    path('api/posts/<uuid:pk>', api_views.post_detail, name="edit_author"),
    path('api/author/posts/<uuid:pk>', api_views.post_detail, name="edit_author"),  # for different groups

    path('api/foreignposts/', api_views.foreignpost_list),
    path('api/image/', api_views.image_detail),

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

    path('authors/friends', respond_to_friends, name="friends"), #TODO: Update

    # Post Modal View
    path('posts/<uuid:pk>', PostDetail.as_view(), name="post_page"),

    # Comment API
    path('api/comments', api_views.comment_list),

    # Home
    path('home/', AuthorList.as_view(), name="home"),
    path('logout/', logout_view, name="logout"),
    path('api_logout/', api_logout, name="api_logout"),

    path('authors/', get_author, name="get_author"),

    # Friend Request
    path('api/friendrequest', AuthorUpdateFriendRequestsView.as_view(), name = "api-friendrequest"),    # how to send a friend request.

    # FRIENDS
    path('api/author/<uuid:pk>/friends/', AuthorfriendsView.as_view(), name="api-friendlist"),      # GET Return query of friends, # POST a list of authors, returns 
    path('api/author/<uuid:pk>/friends/<uuid:pk2>', AuthorIsfriendsView.as_view(), name="api-checkfriends"), # returns a boolean if they are friends
    path('api/author/<uuid:pk>/friendrequest' , AuthorFriendRequestsView.as_view(), name="api-returnfriendrequests"), # Returns all the authors current friend requests.

    # Friend actions
    path('api/author/<uuid:pk>/accept-friend-request', AuthorFriendRequestActionsView.as_view(), {'method': "accept"}, name="accept-friend", ),
    path('api/author/<uuid:pk>/decline-friend-request', AuthorFriendRequestActionsView.as_view(),{'method': "decline"}, name="decline-friend", ),
    path('api/author/<uuid:pk>/send-friend-request', AuthorFriendRequestActionsView.as_view(), {'method': "send-request"}, name="send-request", ),
    path('api/author/<uuid:pk>/unfriend', AuthorFriendRequestActionsView.as_view(),{'method': "unfriend"}, name="unfriend",  ),

    path('docs/', schema_view, name="docs")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
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
from views.author_views import log_in, sign_up, logout_view, get_author, get_authors    
from views import api_views
from Authors.views import AuthorList, AuthorDetail
from Posts.views import PostList, PostDetail
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Login, Signup and Logout
    # path('',log_in), Root should be home if user is logged in
    #path('login/', log_in),
    url( r'^login/$', log_in, name="login"),
    path('signup/', sign_up),

    # Admin
    path('admin/', admin.site.urls),

    # Author API
    path('api/authors/', api_views.Author_list),
    path('api/authors/<uuid:pk>', api_views.Author_detail),

    # Post API
    path('api/posts/', api_views.post_list),
    path('api/posts/<uuid:pk>', api_views.post_detail),

    path('friends/<uuid:pk>', AuthorDetail.as_view()),

    # Search 
    path('search/', get_authors, name="search"),

    # Posts API
    path('api/posts/', PostList.as_view()),
    path('api/posts/<uuid:pk>', PostDetail.as_view()),

    # Author page
    path('authors/<uuid:pk>', AuthorDetail.as_view()),

    # Post Modal View
    path('posts/<uuid:pk>', PostDetail.as_view()),

    # Home
    path('home/', AuthorList.as_view(), name="home"),
    path('logout/', logout_view, name="logout"),

    path('authors/', get_author),



]

# https://docs.djangoproject.com/en/2.1/topics/http/urls/
# https://www.django-rest-framework.org/api-guide/format-suffixes/


urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

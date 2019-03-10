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
from views.general_views import header, homepage
from templates.views.author_views import log_in, sign_up, create_post
from Authors import views
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [
    path('',log_in),
    path('admin/', admin.site.urls),
    path('login/', log_in),
    path('signup/', sign_up),
    path('header/', header),
    path('post/', create_post),
    path('Authors/', views.Author_list),
    
    #https://docs.djangoproject.com/en/2.1/topics/http/urls/
    path('Authors/<int:pk>', views.Author_detail),
    path('home/',homepage),

]

# https://www.django-rest-framework.org/api-guide/format-suffixes/


urlpatterns = format_suffix_patterns(urlpatterns)

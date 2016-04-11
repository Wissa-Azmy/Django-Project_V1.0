"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^create/$', article_create, name='create'),
    url(r'^(?P<id>\d+)/$', article_details, name='details'),
    url(r'^(?P<id>\d+)/update/$', article_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', article_delete, name='delete'),
    url(r'^register$', register, name='register'),
    url(r'^login$', login, name='login'),
    # url(r'^accounts/login/$', name='facelogin'),
    url(r'^auth_login$', auth_view, name='login_auth'),
    url(r'^profile$', user_profile, name='profile'),
    url(r'^editProfile$', editProfile, name='editProfile'),
    url(r'^logout$', logout, name='logout'),	
]

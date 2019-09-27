from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from .views import home, signup, profile, activity


urlpatterns = [
    url(r'home$', home, name='user_home'),
    url(r'^$', home, name='home'),
    url(r'signup', signup, name='signup'),
    url(r'profile', profile, name='profile'),
    url(r'activity', activity, name='activity')
]

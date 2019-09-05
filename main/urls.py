from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from .views import home


urlpatterns = [
    url(r'home$', home, name='user_home'),
    url(r'^$', home, name='home')
]

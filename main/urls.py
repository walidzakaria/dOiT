from django.contrib import admin
from django.db import router
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

from main.viewsets import GetActivityListByUser
from .views import home, signup, profile, activity
from .routers import router
from .api import show_activity_type


urlpatterns = [
    url(r'home$', home, name='user_home'),
    url(r'^$', home, name='home'),
    url(r'^signup$', signup, name='signup'),
    url(r'^profile$', profile, name='profile'),
    url(r'^activity$', activity, name='activity'),
    url(r'^api/', include(router.urls)),
    url(r'^current-user-activity/$', GetActivityListByUser.as_view()),
]

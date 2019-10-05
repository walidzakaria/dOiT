from django.contrib import admin
from django.db import router
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

from .views import home, signup, profile, activity, UserViewSet, ActivityTypeViewSet
from .routers import router
from .api import show_activity_type


urlpatterns = [
    url(r'home$', home, name='user_home'),
    url(r'^$', home, name='home'),
    url(r'^signup$', signup, name='signup'),
    url(r'^profile$', profile, name='profile'),
    url(r'^activity$', activity, name='activity'),
    url(r'^api/', include(router.urls)),
    url(r'^api/show-activity-type', show_activity_type, name='test')
]

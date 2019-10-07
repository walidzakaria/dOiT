#!/usr/bin/env python
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import ActivityType, Activity, Profile, UserActivity, UserActivityAlbum
import django_filters
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.serializers import ModelSerializer
from django.db.models import Q


from .serializers import UserSerializer, ActivityTypeSerializer, ActivitySerializer, UserActivitySerializer, \
    UserFullActivitySerializer
from cloudinary.forms import cl_init_js_callbacks


from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# from .models import City, Country, Hotel, HotelChain, Season, StarRating, Team
import datetime
from django.db.models import Q

from main.forms import UserForm, ProfileForm, SignUpForm, ActivityTypeForm, UserActivityForm, UserCreationForm, \
    UserActivityAlbumForm, ActivityForm


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ActivityTypeViewSet(viewsets.ModelViewSet):
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class UserActivityViewSet(viewsets.ModelViewSet):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer


class UserFullActivityViewSet(viewsets.ModelViewSet):
    queryset = UserActivity.objects.all()
    serializer_class = UserFullActivitySerializer


class GetActivityListByUser(generics.ListAPIView):
    serializer_class = UserFullActivitySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        activities = UserActivity.objects.filter(user=user).all()
        return activities


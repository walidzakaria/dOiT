#!/usr/bin/env python
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import render, redirect
from rest_framework import viewsets, generics
from .models import ActivityType, Activity, Profile, UserActivity, UserActivityAlbum, Deal
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from dal import autocomplete
from django.db.models import Q

from .serializers import UserSerializer, ActivityTypeSerializer, ActivitySerializer, UserActivitySerializer, \
    ActivityFullSerializer, SearchResultSerializer
from cloudinary.forms import cl_init_js_callbacks

from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt

# from .models import City, Country, Hotel, HotelChain, Season, StarRating, Team
import datetime
from django.db.models import Q

from main.forms import UserForm, ProfileForm, SignUpForm, ActivityTypeForm, UserActivityForm, UserCreationForm, \
    UserActivityAlbumForm, ActivityForm


def home(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


@login_required
@transaction.atomic
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home')
        else:
            messages.error(request, 'invalid sign up')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        auth_login(request, user)
        return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# @csrf_exempt
@login_required
@transaction.atomic
def activity(request):
    if request.method == 'POST':

        activity_type_form = ActivityTypeForm(request.POST)
        activity_form = ActivityForm(request.POST)
        user_activity_form = UserActivityForm(request.POST)

        if activity_type_form.is_valid() and activity_form.is_valid() and user_activity_form.is_valid():

            existing_activity_type = ActivityType.objects.filter(
                activity_type=activity_type_form.cleaned_data['activity_type']).first()
            if not existing_activity_type:
                existing_activity_type = ActivityType(activity_type=activity_type_form.cleaned_data['activity_type'])
                existing_activity_type.save()

            activity_form.cleaned_data['activity_type'] = existing_activity_type

            existing_activity = Activity.objects.filter(activity_type=existing_activity_type,
                                                        activity=activity_form.cleaned_data['activity']).first()
            if not existing_activity:
                existing_activity = Activity(activity_type=existing_activity_type,
                                             activity=activity_form.cleaned_data['activity'])
                existing_activity.save()

            user_activity_form.cleaned_data['user'] = request.user
            user_activity_form.cleaned_data['activity'] = existing_activity
            print(existing_activity.activity_id)

            user_activity = UserActivity(user=request.user, activity=existing_activity,
                                         location=user_activity_form.cleaned_data['location'],
                                         lat=user_activity_form.cleaned_data['lat'],
                                         lon=user_activity_form.cleaned_data['lon'],
                                         monday=user_activity_form.cleaned_data['monday'],
                                         tuesday=user_activity_form.cleaned_data['tuesday'],
                                         wednesday=user_activity_form.cleaned_data['wednesday'],
                                         thursday=user_activity_form.cleaned_data['thursday'],
                                         friday=user_activity_form.cleaned_data['friday'],
                                         saturday=user_activity_form.cleaned_data['saturday'],
                                         sunday=user_activity_form.cleaned_data['sunday'],
                                         open_from=user_activity_form.cleaned_data['open_from'],
                                         open_to=user_activity_form.cleaned_data['open_to'],
                                         price=user_activity_form.cleaned_data['price'],
                                         quota=user_activity_form.cleaned_data['quota'],
                                         other=user_activity_form.cleaned_data['other'],
                                         description=user_activity_form.cleaned_data['description'])

            user_activity.save()
            print('saved')
            return redirect('activity')

        else:
            print(user_activity_form.errors)
            messages.error(request, 'invalid input!')
            return redirect('activity')

    elif request.method == 'GET':
        activities = UserActivity.objects.filter(user=request.user).all()
        activity_type_form = ActivityTypeForm()
        activity_form = ActivityForm()
        user_activity_form = UserActivityForm()
        return render(request, 'activity.html', {
            'activities': activities,
            'activity_type_form': activity_type_form,
            'activity_form': activity_form,
            'user_activity_form': user_activity_form
        })


class ActivityTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ActivityType.objects.none()

        qs = ActivityType.objects.all()
        if self.q:
            qs = qs.filter(activity_type__istartswith=self.q)

        return qs


class ActivityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Activity.objects.none()

        qs = Activity.objects.all()
        if self.q:
            activity_type = ActivityType.objects.filter(activity_type=self.q).first()
            qs = Activity.objects.filter(activity_type=activity_type).all()

        return qs


'''
class SearchAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Activity.objects.all().values('activity_id', 'activity_type__activity_type', 'activity_type__activity_type_id', 'activity')

        if self.q:
            qs = qs.filter(
                Q(activity__icontains=self.q) | Q(activity_type__activity_type__icontains=self.q)
            )[0:200]

        return qs
'''


class SearchAutocomplete(generics.ListAPIView):
    serializer_class = ActivityFullSerializer

    def get_queryset(self):
        """
        :returns user search autocomplete api list
        """
        search_string = self.kwargs['search_string']
        search_string = str.replace(search_string, '+', ' ')
        search_string = search_string.strip('')

        return Activity.objects.filter(
            Q(activity_type__activity_type__icontains=search_string) | Q(activity__icontains=search_string)
        ).all()


class SearchResult(generics.ListAPIView):
    serializer_class = SearchResultSerializer

    def get_queryset(self):
        """ returns search result """
        search_string = self.kwargs['search_string']
        search_string = str.replace(search_string, '+', ' ')
        search_string = search_string.strip('')

        user_lat = self.kwargs['user_lat']
        user_lon = self.kwargs['user_lon']
        user_location = (user_lat, user_lon)

        unsorted_activities = UserActivity.objects.filter(
            Q(activity__activity__icontains=search_string) |
            Q(activity__activity_type__activity_type__icontains=search_string)
        ).all()[0:100]

        # sorted_activities = sorted(unsorted_activities, lambda t: t.rating)
        # return sorted_activities
        return unsorted_activities

#!/usr/bin/env python
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

#from .models import City, Country, Hotel, HotelChain, Season, StarRating, Team
import datetime
from django.db.models import Q

from main.forms import UserForm, ProfileForm, ActivityForm


def home(request):
    return render(request, 'index.html')


#def signup(request):
#    return render(request, 'signup.html')


def profile(request):
    return render(request, 'profile.html')


def activity(request):
    return render(request, 'activity.html')


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_from = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_from.is_valid() and profile_form.is_valid():
            user_from.save()
            profile_form.save()
            #messages.success(request, 'Your profile saved successfully!')
            return redirect('home')
        else:
            pass
            #messages.error(request, _('Please correct the error below.'))
    else:
        user_from = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_from,
        'profile_form': profile_form
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
@transaction.atomic
def activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ActivityForm()
        return render(request, 'activity.html', {'form': form})


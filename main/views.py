#!/usr/bin/env python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

#from .models import City, Country, Hotel, HotelChain, Season, StarRating, Team
import datetime
from django.db.models import Q


def home(request):
    return render(request, 'index.html')


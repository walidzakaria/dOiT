from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.utils import json

from .models import ActivityType


def show_activity_type(request):
    activity_type = ActivityType.objects.all().values('activity_type_id', 'activity_type')
    result = list(activity_type)
    return JsonResponse(result, safe=False)

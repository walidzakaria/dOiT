from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.utils import json

from .models import ActivityType, Activity, Employee, Deal


def show_employee(request):
    employees = Employee.objects.all()
    result = list(employees)

    return JsonResponse(result, safe=False)

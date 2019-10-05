from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import ActivityType, Activity, UserActivity, Profile, UserActivityAlbum, Deal
from django_filters import rest_framework as filters


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ActivityTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ActivityType
        fields = '__all__'

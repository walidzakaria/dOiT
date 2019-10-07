from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import ActivityType, Activity, UserActivity, Profile, UserActivityAlbum, Deal
from drf_writable_nested import WritableNestedModelSerializer
from django_filters import rest_framework as filters


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = '__all__'

    def create(self, validated_data):
        """ This is to override the normal saving, and avoids duplication """
        existing_object = ActivityType.objects.filter(activity_type=validated_data['activity_type']).first()
        if not existing_object:
            new_object = ActivityType(activity_type=validated_data['activity_type'])
            new_object.save()
            return new_object
        return existing_object


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

    def create(self, validated_data):
        """ This is to override the normal saving, and avoids duplication """
        existing_object = Activity.objects.filter(activity_type=validated_data['activity_type'], activity=validated_data['activity']).first()
        if not existing_object:
            new_object = Activity(activity_type=validated_data['activity_type'], activity=validated_data['activity'])
            new_object.save()
            return new_object
        return existing_object


class ActivityFullSerializer(serializers.ModelSerializer):
    activity_type = ActivityTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'


class UserFullActivitySerializer(WritableNestedModelSerializer):
    activity = ActivityFullSerializer(many=False, read_only=True)

    class Meta:
        model = UserActivity
        fields = '__all__'

from rest_framework import serializers, request, generics
from django.contrib.auth.models import User, Group
from .models import ActivityType, Activity, UserActivity, Profile, UserActivityAlbum, Deal
from drf_writable_nested import WritableNestedModelSerializer
from django_filters import rest_framework as filters
import urllib.request, json
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User, Group


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

    def create(self, validated_data):
        # validated_data['user'] = 1
        # app_id = '35mHfJ3nOmgsSR7Om5tn'
        # app_code = 'dXMLSO7UYuvI6U0Ns_OmRQ'
        # search_text = str.replace(validated_data['location'], ' ', '+')
        # url = f'https://geocoder.api.here.com/6.2/geocode.json?app_id={app_id}&app_code={app_code}&searchtext={search_text}'
        # print(url)
        # response = urllib.request.urlopen(url)
        # data = json.loads(response.read())
        # print(data.Response.View[0].Result[0])
        # validated_data['user'] = self.request.user
        # print(validated_data['user'])
        current_user = serializers.SerializerMethodField('_user')

        # Use this method for the custom field
        def _user(self, obj):
            request = getattr(self.context, 'request', None)
            if request:
                return request.user

        # validated_data['user'] = current_user
        print(current_user)
        return UserActivity.objects.create(**validated_data)


class FullActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    activity_type = serializers.CharField(max_length=100)
    activity = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=200)
    lon = serializers.FloatField()
    lat = serializers.FloatField()
    monday = serializers.BooleanField(default=True)
    tuesday = serializers.BooleanField(default=True)
    wednesday = serializers.BooleanField(default=True)
    thursday = serializers.BooleanField(default=True)
    friday = serializers.BooleanField(default=True)
    saturday = serializers.BooleanField(default=False)
    sunday = serializers.BooleanField(default=False)
    open_from = serializers.TimeField()
    open_to = serializers.TimeField()
    description = serializers.CharField(max_length=350)

    def create(self, validated_data):
        existing_type = ActivityType.objects.filter(activity_type=validated_data['activity_type'])
        if not existing_type:
            existing_type = ActivityType(activity_type=validated_data['activity_type'])
            existing_type.save()
        existing_activity = Activity.objects.filter(activity_type=existing_type, activity=validated_data['activity'])
        if not existing_activity:
            existing_activity = Activity(activity_type=existing_type, activity=validated_data['activity'])
        activity_user = User.objects.filter(username=validated_data['username'])
        print(activity_user.id)
        new_activity = UserActivity(user=activity_user.id, activity=existing_activity, location=validated_data['location'],
                                    lat=validated_data['lat'], lon=validated_data['lon'], monday=validated_data['monday'],
                                    tuesday=validated_data['tuesday'], wednesday=validated_data['wednesday'],
                                    thursday=validated_data['thursday'], friday=validated_data['friday'],
                                    saturday=validated_data['saturday'], sunday=validated_data['sunday'],
                                    open_from=validated_data['open_from'], open_to=validated_data['open_to'],
                                    description=validated_data['description'])
        new_activity.save()
        return new_activity

    def update(self, instance, validated_data):
        existing_type = ActivityType.objects.filter(activity_type=validated_data['activity_type'])
        if not existing_type:
            existing_type = ActivityType(activity_type=validated_data['activity_type'])
            existing_type.save()
        existing_activity = Activity.objects.filter(activity_type=existing_type, activity=validated_data['activity'])
        if not existing_activity:
            existing_activity = Activity(activity_type=existing_type, activity=validated_data['activity'])

        activity_instance = UserActivity.objects.get(pk=validated_data['id'])
        activity_instance.activity = validated_data['activity']
        activity_instance.location = validated_data['location']
        activity_instance.lon = validated_data['lon']
        activity_instance.lat = validated_data['lat']
        activity_instance.monday = validated_data['monday']
        activity_instance.tuesday = validated_data['tuesday']
        activity_instance.wednesday = validated_data['wednesday']
        activity_instance.thursday = validated_data['thursday']
        activity_instance.friday = validated_data['friday']
        activity_instance.saturday = validated_data['saturday']
        activity_instance.sunday = validated_data['sunday']
        activity_instance.open_from = validated_data['open_from']
        activity_instance.open_to = validated_data['open_to']
        activity_instance.description = validated_data['description']
        activity_instance.save()
        return activity_instance


class UserFullActivitySerializer(WritableNestedModelSerializer):
    activity = ActivityFullSerializer(many=False, read_only=True)

    class Meta:
        model = UserActivity
        fields = '__all__'




from rest_framework import serializers
from .models import ActivityType, Activity, Employee
from django_filters import rest_framework as filters


class SearchResult(serializers.ModelSerializer):

    #rating = StarRatingSerializer(many=False, read_only=True)
    #city = CitySerializer(many=False, read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

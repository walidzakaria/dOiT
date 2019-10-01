from django.contrib.contenttypes import forms

from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'location', 'birth_date', 'activity',
                  'phone', 'lat', 'lon', 'score', 'description',
                  'profile_picture')

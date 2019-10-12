from django.contrib.auth.forms import UserCreationForm
from django.contrib.contenttypes import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Textarea, widgets


from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'birth_date',
                  'phone', 'score', 'profile_picture')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ActivityTypeForm(forms.ModelForm):
    class Meta:
        model = ActivityType
        fields = ('activity_type',)


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('activity',)


class UserActivityForm(forms.ModelForm):
    class Meta:
        model = UserActivity
        fields = ('location', 'lat', 'lon',
                  'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
                  'open_from', 'open_to', 'description')
        readonly_fields = ('rating', 'deals',)
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 3}),
        }


class UserActivityAlbumForm(forms.ModelForm):
    class Meta:
        model = UserActivityAlbum
        fields = ('photo',)
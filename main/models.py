from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHOICE = (
    ('M', 'Male'),
    ('F', 'Female')
)


class ActivityType(models.Model):
    activity_type_id = models.AutoField(primary_key=True)
    activity_type = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.activity_type


class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    activity = models.CharField(max_length=100, db_index=True)

    class Meta:
        verbose_name_plural = 'activities'

    def __str__(self):
        return self.activity


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, default='M', choices=GENDER_CHOICE)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    join_date = models.DateField(auto_now_add=True)
    activity = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    lat = models.CharField(max_length=30, null=True, blank=True)
    lon = models.CharField(max_length=30, null=True, blank=True)
    score = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='images/', default='images/default-profile.png')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField

GENDER_CHOICE = (
    ('M', 'Male'),
    ('F', 'Female')
)

REQUEST_CHOICE = (
    ('R', 'Request'),
    ('A', 'Accepted'),
    ('D', 'Declined'),
    ('F', 'Finished')
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
    phone = models.CharField(max_length=20, null=True, blank=True)
    score = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    profile_picture = CloudinaryField('image')

    # activity = models.CharField(max_length=100, null=True, blank=True)
    # lat = models.CharField(max_length=30, null=True, blank=True)
    # lon = models.CharField(max_length=30, null=True, blank=True)

    # description = models.CharField(max_length=250, null=True, blank=True)
    # profile_picture = models.ImageField(upload_to='images/', default='images/default-profile.png')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    lat = models.CharField(max_length=100)
    lon = models.CharField(max_length=100)
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    open_from = models.TimeField()
    open_to = models.TimeField()


class UserActivityAlbum(models.Model):
    user_activity = models.ForeignKey(UserActivity, on_delete=models.CASCADE)
    photo = CloudinaryField('image')


class Deal(models.Model):
    request_from = models.ForeignKey(User, on_delete=models.CASCADE)
    request_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_to")
    request_date = models.DateTimeField(auto_now_add=True)
    request_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='R', choices=REQUEST_CHOICE)
    rating = models.IntegerField(default=5)
    review = models.TextField(null=True, blank=True)

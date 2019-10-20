from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from geopy.distance import geodesic

GENDER_CHOICE = (
    ('M', 'Male'),
    ('F', 'Female')
)

REQUEST_CHOICE = (
    ('R', 'Request'),
    ('C', 'Cancelled'),
    ('A', 'Accepted'),
    ('D', 'Declined'),
    ('F', 'Finished')
)

WORK_PER_CHOICE = (
    ('D', 'Per Day'),
    ('W', 'Per Week'),
    ('H', 'Per Hour'),
    ('P', 'Per Piece'),
    ('V', 'Per Visit'),
    ('O', 'Other')
)


class ActivityType(models.Model):
    activity_type_id = models.BigAutoField(primary_key=True)
    activity_type = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.activity_type


class Activity(models.Model):
    activity_id = models.BigAutoField(primary_key=True)
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
    profile_picture = CloudinaryField('image')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class UserActivity(models.Model):
    user_activity_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    open_from = models.TimeField()
    open_to = models.TimeField()
    price = models.DecimalField(decimal_places=2, max_digits=14, blank=True, null=True)
    quota = models.CharField(max_length=1, default='D', choices=WORK_PER_CHOICE, null=True, blank=True)
    other = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=350)

    @property
    def rating(self):
        user_rating = Deal.objects.filter(user_activity=self).filter(status='F').aggregate(Avg('rating'))
        if user_rating['rating__avg'] is None:
            user_rating = 0
        else:
            user_rating = user_rating['rating__avg']

        return user_rating

    @property
    def deals(self):
        user_deals = Deal.objects.filter(user_activity=self).filter(status='F').count()
        return user_deals

    def distance(self, other_location):
        deal_location = (self.lat, self.lon)
        result = geodesic(deal_location, other_location).kilometers
        return result

    def __str__(self):
        return f'User: {self.user.username}, Activity: {self.activity.activity}'


class UserActivityAlbum(models.Model):
    user_activity_album_id = models.BigAutoField(primary_key=True)
    user_activity = models.ForeignKey(UserActivity, on_delete=models.CASCADE)
    photo = CloudinaryField('image')


class Deal(models.Model):
    deal_id = models.BigAutoField(primary_key=True)
    user_activity = models.ForeignKey(UserActivity, on_delete=models.CASCADE)
    request_from = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    request_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='R', choices=REQUEST_CHOICE)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    question = models.CharField(max_length=300, blank=True, null=True)
    rating = models.IntegerField(default=5)
    review = models.TextField(null=True, blank=True)


class Chat(models.Model):
    chat_id = models.BigAutoField(primary_key=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f'User {self.user.username}, on {self.time}: {self.chat} ({self.seen})'


class SearchLog(models.Model):
    search_log_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_date = models.DateTimeField(auto_now_add=True)
    search_text = models.CharField(max_length=300, db_index=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'User: {self.user.username}, Search: {self.search_text}'
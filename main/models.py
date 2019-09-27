from django.contrib.auth.models import User
from django.db import models


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


class Employee(models.Model):
    employee_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, default='male')
    join_date = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=20)
    security_question = models.CharField(max_length=100)
    security_answer = models.CharField(max_length=150)

    def __str__(self):
        return self.user.username


class EmployeeActivity(models.Model):
    employee_activity_id = models.BigAutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    lat = models.CharField(max_length=30)
    lon = models.CharField(max_length=30)
    score = models.DecimalField(max_digits=10, decimal_places=4)
    description = models.CharField(max_length=250)
    working_days = models.CharField(max_length=50)
    #start_hour = models.TimeField()
    #end_hour = models.TimeField()


class Deal(models.Model):
    deal_id = models.BigAutoField(primary_key=True)
    deal_time = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=5)
    rating = models.IntegerField()
    comment = models.CharField(max_length=250)

    def __str__(self):
        return f'id: {self.deal_id}: user: {self.employee.employee_id}'



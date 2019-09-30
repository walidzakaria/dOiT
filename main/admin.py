from django.contrib import admin
from .models import ActivityType, Activity, Employee, Deal

'''
@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('activity_type_id', 'activity_type')
    list_editable = ('activity_type',)
    search_fields = ('activity_type_id', 'activity_type')
    list_per_page = 20


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_id', 'activity_type', 'activity')
    list_editable = ('activity_type', 'activity')
    search_fields = ('activity_id', 'activity_type', 'activity')
    list_per_page = 20


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'profile', 'lat', 'long', 'activity',
                    'rating', 'description', 'join_date', 'phone')

    list_editable = ('user', 'profile', 'lat', 'long', 'activity',
                     'rating', 'description', 'phone')

    search_fields = ('employee_id', 'user', 'profile', 'lat', 'long', 'activity',
                     'rating', 'description', 'join_date', 'phone')
    list_per_page = 20


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('deal_id', 'deal_time', 'employee', 'guest', 'status', 'rating')
    list_editable = ('employee', 'guest', 'status', 'rating')
    search_fields = ('deal_id', 'deal_time', 'employee', 'guest', 'status', 'rating')
    list_per_page = 20
'''

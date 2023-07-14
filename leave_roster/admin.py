from django.contrib import admin
from . models import LeaveRoster

class LeaveRosterAdmin(admin.ModelAdmin):
    list_display = ['staff', 'type_of_leave', 'number_of_days', 'date_applied', 'start_date', 'end_date', 'status']
admin.site.register(LeaveRoster, LeaveRosterAdmin)

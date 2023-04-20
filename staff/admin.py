from django.contrib import admin
from .models import Employee, Skill
from django.http import HttpResponse
import csv


def generate_employee_records(modeladmin, request, queryset):
    headers  =["EMPLOYEE NAME", "NICKNAME", "DATE OF BIRTH", "PLACE OF BIRTH", "GENDER", "NATIONALITY", "MARITAL STATUS", "SPOUSE", "NATIONAL ID",
                "PASSPORT", "DRIVERS LICENSE", "VOTERS ID", "ACCOUNT NAME", "BANK", "SWIFT CODE", "ACCOUNT NUMBER", "COUNTRY", "STREET", 
                "CITY", "ZIP CODE", "CUG NUMBER", "MOBILE 1", "MOBILE 2", "PERSONAL EMAIL", "WORK EMAIL", "HIRED DATE", "RESIGNED DATE",
                "CONTRACT COMMENCE", "CONTRACT END", "DEPARTMEN", "TITLE", "CLASSIFICATION"]
    
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="employee_records.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(["EMPLOYEE DATABASE"])
    writer.writerow(headers)
    cr = queryset.values_list('employee_name', 'nickname', 'date_of_birth', 'place_of_birth', 'gender', 'nationality',
                                'marital_status', 'spouse', 'national_id', 'passport', 'drivers_license', 'voters_id',
                                'account_name', 'bank', 'swift_code', 'account_number', 'country', 'street', 'city', 'zip_code', 
                                'cug_number', 'mobile_1', 'mobile_2', 'personal_email', 'work_email', 'hired_date', 'resigned_date', 
                                'contract_commence', 'contract_end', 'department', 'title', 'classification')
    for r in cr:
        writer.writerow(r)
    return response

generate_employee_records.short_description = 'Export Employee Record as csv'

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'employee_name','nickname', 'country', 'date_of_birth', 'place_of_birth', 'gender', 'nationality', 
                    'work_email', 'hired_date', 'employment_status']
    search_fields = ['staff_id', 'employee_name','nickname', 'country', 'date_of_birth', 'place_of_birth', 'gender', 'nationality', 
                     'work_email', 'hired_date', 'employment_status']
    sortable_by = ['staff_id', 'employee_name','nickname', 'country', 'date_of_birth', 'place_of_birth', 'gender', 'nationality',
                    'work_email', 'hired_date', 'employment_status']
    filter_by = ['staff_id', 'employee_name','nickname', 'country', 'date_of_birth', 'place_of_birth', 'gender', 'nationality', 'work_email',
                  'hired_date', 'emp_status']
    list_filter = ['place_of_birth', 'gender', 'nationality', 'hired_date', 'employment_status']

    fieldsets = (
        ('Personal Details', {
            'classes': ('collapse',),
            'fields': ('image', 'employee_name', 'nickname', 'date_of_birth', 'place_of_birth', 'gender', 'staff_id', 'tin', 'sshfc', 'nationality', 'marital_status', 'spouse', 'national_id', 'passport', 'drivers_license', 'voters_id', 'account_name', 'bank', 'swift_code', 'account_number', 'skills', 'facebook_link', 'instagram_link', 'twitter_link', 'linkedin_link')
        }),
        ('Contact details', {
            'classes': ('collapse',),
            'fields': ('country', 'street', 'city', 'zip_code', 'cug_number', 'mobile_1', 'mobile_2', 'personal_email', 'work_email')
        }),
        ('Job details', {
            'classes': ('collapse',),
            'fields': ('department', 'classification', 'title', 'hired_date', 'resigned_date', 'contract_commence', 'contract_end', 'employment_status', 'probation_commence', 'probation_end', 'warning')
        }),
    )
    actions = [generate_employee_records]
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Skill)
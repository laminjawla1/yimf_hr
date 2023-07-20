from django.contrib import admin
from .models import Payroll
from django.http import HttpResponse
import csv


def generate_payroll_records(modeladmin, request, queryset):
    headers  =["EMPLOYEE", "BASIC SALARY", "MEDICAL ALLOWANCE", "TRANSPORT ALLOWANCE", "RESPONSIBILITY ALLOWANCE", 
               "HOUSING ALLOWANCE", "RISK ALLOWANCE", "GROSS PAY", "INCOME TAX", "SSHFC", "INDIVIDUAL SSHFC", "DEDUCTION", "ICF", "REFUND" "NET PAY", "DEDUCTION TYPE"]
    
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="employee_payroll_records.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(["EMPLOYEE PAYROLL"])
    writer.writerow(headers)
    cr = queryset.values_list('employee__employee_name', 'basic_salary', 'medical_allowance', 'transport_allowance', 'responsibility_allowance',
                               'housing_allowance', 'risk_allowance', 'gross_pay', 'income_tax', 'sshfc', 'individual_sshfc', 'deduction', 'icf', 'refund',
                                'net_pay', 'deduction_type')
    for r in cr:
        writer.writerow(r)
    return response

generate_payroll_records.short_description = "Export Payroll as CSV"

class PayrollAdmin(admin.ModelAdmin):
    list_display = ['employee', 'basic_salary', 'medical_allowance', 'transport_allowance', 'responsibility_allowance', 
                    'housing_allowance', 'risk_allowance', 'gross_pay', 'income_tax', 'sshfc', 'individual_sshfc', 'deduction', 'deduction_type', 'icf', 'refund', 'net_pay', 'date']
    search_fields = ['employee']
    sortable_by = ['employee', 'deduction_type', 'date']
    list_filter = ['date', 'employee']
    readonly_fields = ['medical_allowance', 'transport_allowance', 'responsibility_allowance', 
                    'housing_allowance', 'gross_pay', 'income_tax', 'sshfc', 'individual_sshfc', 'deduction', 'deduction_type', 'icf', 'refund', 'net_pay', 'date']
    
    actions = [generate_payroll_records]

admin.site.register(Payroll, PayrollAdmin)
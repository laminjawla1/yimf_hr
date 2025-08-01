from django import forms
from .models import Payroll
from staff.models import Employee

class PayrollForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PayrollForm, self).__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employee.objects.all().exclude(employment_status__in=["Resigned", "Fired"]).order_by("employee_name")
        self.fields['date'].widget=forms.DateInput(attrs={'type': 'date'})

    class Meta:
        model = Payroll
        fields = [
            'date',
            'employee',
            'basic_salary',
            'risk_allowance',
            'provincial_allowance',
            'income_tax',
            'staff_fin',
            'refund',
            'deduction',
            'deduction_type'
        ]

class FilterPayrollForm(forms.Form):
    staff = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Employee'}))
    staff_id = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Staff ID'}))
    date = forms.DateTimeField(label="", required=False, widget=forms.DateInput(attrs={'type': 'date'}))

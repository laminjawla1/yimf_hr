from django import forms
from .models import Payroll
from staff.models import Employee

class PayrollForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PayrollForm, self).__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employee.objects.all().exclude(employment_status__in=["Resigned", "Fired"]).order_by("employee_name")
    class Meta:
        model = Payroll
        fields = ['employee', 'basic_salary', 'income_tax', 'staff_fin', 'deduction', 'deduction_type']

class FilterPayrollForm(forms.Form):
    staff = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Employee'}))
    staff_id = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Staff ID'}))
    date = forms.DateTimeField(label="", required=False, widget=forms.DateInput(attrs={'type': 'date'}))

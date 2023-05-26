from django import forms
from .models import Payroll

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['employee', 'basic_salary', 'income_tax', 'staff_fin', 'deduction', 'deduction_type']

class FilterPayrollForm(forms.Form):
    employee = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Employee'}))
    staff_id = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Staff ID'}))
    date = forms.DateTimeField(label="", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    widgets = {
            'my_date': forms.DateInput()
        }

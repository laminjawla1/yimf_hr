from django import forms
from . models import LeaveRoster
from staff.models import Employee

class FilterLeaves(forms.Form):
    employee = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Employee'}))
    department = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Department'}))
    date = forms.DateTimeField(label="", required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class LeaveApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LeaveApplicationForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget=forms.DateInput(attrs={'type': 'date'})
        self.fields['staff'].queryset = Employee.objects.all().exclude(employment_status__in=["Resigned", "Fired"]).order_by("employee_name")
    class Meta:
        model = LeaveRoster
        fields = ['staff', 'type_of_leave', 'number_of_days', 'start_date', 'leave_reason']
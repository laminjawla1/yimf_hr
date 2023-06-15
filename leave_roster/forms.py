from django import forms
from . models import LeaveRoster

class FilterLeaves(forms.Form):
    employee = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Employee'}))
    department = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Department'}))
    date = forms.DateTimeField(label="", required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class LeaveApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LeaveApplicationForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget=forms.DateInput(attrs={'type': 'date'})
    class Meta:
        model = LeaveRoster
        fields = ['type_of_leave', 'number_of_days', 'start_date', 'leave_reason']
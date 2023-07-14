import datetime
from typing import Optional, Type

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.forms.models import BaseModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from staff.models import Employee

from .forms import FilterLeaves, LeaveApplicationForm
from .models import LeaveRoster
from django.core.exceptions import PermissionDenied
from django.views.generic import UpdateView
from django import forms


# Create your views here.
def leave_roster(request):
    leave_roster = LeaveRoster.objects.order_by('-date_applied')
    page = request.GET.get('page', 1)
    
    if request.method == 'POST':
        leave_form = LeaveApplicationForm(request.POST)
        leave_filter = FilterLeaves(request.POST)
        if leave_form.is_valid():
            if leave_form.instance.type_of_leave == "Annual":
                if leave_form.instance.staff.total_leave_balance - leave_form.instance.number_of_days < 0:
                    messages.error(request, f"Sorry, {leave_form.instance.staff} has exausted his/her allocated annual leave")
                    return HttpResponseRedirect(reverse('leave_roster'))
            leave_form.instance.end_date = leave_form.instance.start_date + datetime.timedelta(days=leave_form.instance.number_of_days)
            leave_form.save()
            messages.success(request, "Leave request added successfully.")
        if leave_filter.is_valid():
            if leave_filter.cleaned_data.get('employee') or leave_filter.cleaned_data.get('department') or leave_filter.cleaned_data.get('date'):
                _date = leave_filter.cleaned_data.get('date')
                if _date:
                    leave_roster = leave_roster.filter(date_applied__year=_date.year, date_applied__month=_date.month).all().order_by('-date_applied')
                leave_roster = leave_roster.filter(
                    staff__first_name__icontains=leave_filter.cleaned_data.get('employee'),
                    staff__profile__staff_profile__department__name__icontains=leave_filter.cleaned_data.get('department')
                ).all().order_by('-date_applied')
    paginator = Paginator(leave_roster, 10)
    try:
        leave_roster = paginator.page(page)
    except:
        leave_roster = paginator.page(1)
    if not leave_roster:
        messages.error(request, "You have no history of leave applications")
    return render(request, "leave_roster/leave_roster.html", {
        'leave_roster': leave_roster, 'filter_form': FilterLeaves, 'current_page': 'leave_roster', 'leave_form': LeaveApplicationForm
    })

def leave_detail(request, leave_id):
    leave = LeaveRoster.objects.filter(id=leave_id).first()
    if leave:
        if request.method == 'POST':
            status = request.POST.get('status')
            if status == 'Approved':
                leave.status = status
                if status == 'Approved':
                    leave.approved = True
                    if leave.type_of_leave == 'Annual':
                        leave.staff.total_leave_balance -= leave.number_of_days
                        leave.staff.total_annual_leave_days_taken += leave.number_of_days
                leave.staff.total_days_of_leave_taken += leave.number_of_days
                leave.save()
                leave.staff.save()
                messages.success(request, f"Leave {status.lower()} successfully.")
                return HttpResponseRedirect(reverse('leave_roster'))
        return render(request, 'leave_roster/leave.html', {
            'leave': leave,'current_page': 'leave_roster'
        })
    messages.error(request, "No valid leave object waas found.")
    return HttpResponseRedirect(reverse('leave_roster'))


class UpdateLeave(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LeaveRoster
    fields = ['staff', 'type_of_leave', 'number_of_days', 'start_date', 'leave_reason']

    def form_valid(self, form):
        form.instance.end_date = form.instance.start_date + datetime.timedelta(days=form.instance.number_of_days)
        messages.success(self.request, "Leave request updated successfully.")
        return super().form_valid(form)
    
    def test_func(self):
        leave = self.get_object()
        return not leave.status == "Approved"
    
    def get_context_data(self, *args, **kwargs):
        context = super(UpdateLeave, self).get_context_data(*args, **kwargs)
        context['button'] = 'Update'
        context['legend'] = 'Update Leave'
        context['current_page'] = 'leave_roster'
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget=forms.DateInput(attrs={'type': 'date'})
        form.fields['staff'].queryset = Employee.objects.all().exclude(employment_status__in=["Resigned", "Fired"]).order_by("employee_name")
        return form
import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from staff.models import Employee

from .forms import FilterLeaves, LeaveApplicationForm
from .models import LeaveRoster
from django.core.exceptions import PermissionDenied
from django.views.generic import UpdateView
from django.contrib.auth.models import User


# Create your views here.
def leave_roster(request):
    leave_roster = LeaveRoster.objects.filter(staff=request.user).order_by('-date_applied')
    page = request.GET.get('page', 1)
    
    if request.method == 'POST':
        leave_form = LeaveApplicationForm(request.POST)
        leave_filter = FilterLeaves(request.POST)
        if leave_form.is_valid():
            leave_form.instance.staff = request.user
            if leave_form.instance.type_of_leave == "Annual":
                if leave_form.instance.staff.profile.staff_profile.total_leave_balance - leave_form.instance.number_of_days < 0:
                    messages.error(request, "Sorry, you have exausted your allocated annual leave")
                    return HttpResponseRedirect(reverse('leave_roster'))
            leave_form.instance.status = "Immediate Supervisor"
            leave_form.instance.end_date = leave_form.instance.start_date + datetime.timedelta(days=leave_form.instance.number_of_days)
            leave_form.save()
            send_mail(
                f'Request For Leave: {leave_form.instance.staff.first_name} {leave_form.instance.staff.last_name}',
                f"""Dear {leave_form.instance.staff.profile.immediate_supervisor.first_name} {leave_form.instance.staff.profile.immediate_supervisor.last_name},
A staff has requested for a leave. Please find details about the application below.

Type Of Leave: {leave_form.instance.type_of_leave}
Number of Days: {leave_form.instance.number_of_days}
Start Date: {leave_form.instance.start_date}
End Date: {(leave_form.instance.start_date + datetime.timedelta(days=leave_form.instance.number_of_days)).strftime('%Y-%m-%d')}

                                            LEAVE REASON
{leave_form.instance.leave_reason}

Link to the leave request: {request.build_absolute_uri()}
                """, 
                f'{request.user.email}',
                [leave_form.instance.staff.profile.immediate_supervisor.email],
                fail_silently=False,
            )
            messages.success(request, "Leave applied successfully. Your Immediate Supervisor will review it sortly.")
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


def leave_requests(request):
    #     leave_roster = LeaveRoster.objects.filter(staff=request.user).order_by('-date_applied')
    if request.user.profile.is_supervisor:
        leave_roster = LeaveRoster.objects.filter(
            staff__profile__immediate_supervisor=request.user,
            status="Immediate Supervisor"
        ).order_by('-date_applied')
    elif request.user.profile.is_hod:
        leave_roster = LeaveRoster.objects.filter(
            staff__profile__staff_profile__department__head=request.user,
            status="Head Of Department"
        ).order_by('-date_applied')
    else:
        if request.user.is_staff:
            leave_roster = LeaveRoster.objects.all().order_by('-date_applied')
        else:
            raise PermissionDenied()
    page = request.GET.get('page', 1)
    
    if request.method == 'POST':
        leave_filter = FilterLeaves(request.POST)
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
    return render(request, "leave_roster/leave_requests.html", {
        'leave_roster': leave_roster, 'filter_form': FilterLeaves, 'current_page': 'leave_roster', 'leave_form': LeaveApplicationForm
    })

def leave_detail(request, leave_id):
    leave = LeaveRoster.objects.filter(id=leave_id).first()
    if leave:
        staff = Employee.objects.filter(staff_id=leave.staff.profile.staff_profile.staff_id)
        if not staff:
            messages.error(request, "No recognize staff is associated with that leave.")
            return HttpResponseRedirect(reverse('leave_roster'))
        
        # Changing leave status
        if request.method == 'POST':
            statuses = [
                'Applicant', 'Immediate Supervisor', 'Head Of Department', 'Rejected','Approved', 'HR Office',
            ]
            status = request.POST.get('status')
            email_message = request.POST.get('email_message')
            if not (status in statuses):
                messages.error(request, 'Invalid status')
                return HttpResponseRedirect(reverse('leave_detail', args=[leave_id]))
            # Unendorsing the leave
            if status == 'Applicant':
                send_mail(
                    f'Leave Unendorsement: {leave.staff.first_name} {leave.staff.last_name}',
                    f"""
{email_message}
Link to the leave request: {request.build_absolute_uri()}
                    """, 
                    f'{request.user.email}',
                    [leave.staff.email],
                    fail_silently=False,
                )
                leave.status = status
                leave.save()
                messages.success(request, "Leave unendorsed successfully.")

            # Resubmitting the leave
            if status == 'Immediate Supervisor' and not request.user.profile.is_hod:
                send_mail(
                    f'Leave Resubmission: {leave.staff.first_name} {leave.staff.last_name}',
                    f"""
{email_message}
Link to the leave request: {request.build_absolute_uri()}
                    """, 
                    f'{request.user.email}',
                    [leave.staff.profile.immediate_supervisor.email],
                    fail_silently=False,
                )
                leave.status = status
                leave.save()
                messages.success(request, "Leave resubmitted successfully.")

            # Unendorsing the leave
            if status == 'Immediate Supervisor' and request.user.profile.is_hod:
                send_mail(
                    f'Leave Unendorsement: {leave.staff.first_name} {leave.staff.last_name}',
                    f"""
{email_message}
Link to the leave request: {request.build_absolute_uri()}
                    """, 
                    f'{request.user.email}',
                    [leave.staff.profile.immediate_supervisor.email],
                    fail_silently=False,
                )
                leave.status = status
                leave.save()
                messages.success(request, "Leave unendorsed successfully.")

            # Endorsing the leave
            if status == 'Head Of Department':
                send_mail(
                    f'Leave Endorsement: {leave.staff.first_name} {leave.staff.last_name}',
                    f"""
{email_message}
Link to the leave request: {request.build_absolute_uri()}
                    """, 
                    f'{request.user.email}',
                    [leave.staff.profile.staff_profile.department.head.email],
                    fail_silently=False,
                )
                leave.status = status
                leave.save()
                messages.success(request, "Leave endorsed successfully.")

            # Endorsing the leave
            if status == 'HR Office':
                hr = User.objects.filter(profile__is_hr=True).first()
                if not hr:
                    messages.error(request, "Sorry, HR is not registered in the system.")
                    return HttpResponseRedirect(reverse('leave_roster'))
                send_mail(
                    f'Leave Endorsement: {leave.staff.first_name} {leave.staff.last_name}',
                    f"""
{email_message}
Link to the leave request: {request.build_absolute_uri()}
                    """, 
                    f'{request.user.email}',
                    [hr.email],
                    fail_silently=False,
                )
                leave.status = status
                leave.save()
                messages.success(request, "Leave endorsed successfully.")

            # Endorsing or unendorsing the leave
            if status == 'Approved' or status == 'Rejected':
                send_mail(
                    f'Leave {status}: {leave.staff.first_name} {leave.staff.last_name}',
                    f"""
{email_message}
Link to the leave request: {request.build_absolute_uri()}
                    """, 
                    f'{request.user.email}',
                    [leave.staff.email],
                    fail_silently=False,
                )
                leave.status = status
                if status == 'Approved':
                    leave.approved = True
                    if leave.type_of_leave == 'Annual':
                        leave.staff.profile.staff_profile.total_leave_balance -= leave.number_of_days
                        leave.staff.profile.staff_profile.total_annual_leave_days_taken += leave.number_of_days
                leave.staff.profile.staff_profile.total_days_of_leave_taken += leave.number_of_days
                leave.save()
                messages.success(request, f"Leave {status.lower()} successfully.")


        return render(request, 'leave_roster/leave.html', {
            'leave': leave, 'staff': staff, 'current_page': 'leave_roster'
        })
    messages.error(request, "No valid leave object waas found.")
    raise HttpResponseRedirect(reverse('leave_roster'))


class UpdateLeave(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LeaveRoster
    fields = ['type_of_leave', 'number_of_days', 'start_date', 'leave_reason']

    def form_valid(self, form):
        form.instance.staff = self.request.user
        form.instance.end_date = form.instance.start_date + datetime.timedelta(days=form.instance.number_of_days)
        messages.success(self.request, "Leave request updated successfully.")
        return super().form_valid(form)
    
    def test_func(self):
        leave = self.get_object()
        return not leave.approved and leave.staff == self.request.user
    
    def get_context_data(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionDenied()
        context = super(UpdateLeave, self).get_context_data(*args, **kwargs)
        context['button'] = 'Update'
        context['legend'] = 'Update Leave'
        context['current_page'] = 'leave_roster'
        return context
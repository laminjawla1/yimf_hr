import datetime

from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from staff.models import Employee

from .forms import FilterLeaves, LeaveApplicationForm
from .models import LeaveRoster


# Create your views here.
def leave_roster(request):
    if request.user.is_superuser:
        leave_roster = LeaveRoster.objects.all().order_by('-date_applied')
    else:
        leave_roster = LeaveRoster.objects.filter(staff=request.user).order_by('-date_applied')
    page = request.GET.get('page', 1)
    
    if request.method == 'POST':
        leave_form = LeaveApplicationForm(request.POST)
        leave_filter = FilterLeaves(request.POST)
        if leave_form.is_valid():
            leave_form.instance.staff = request.user
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
                'yonnatech.g@gmail.com',
                [leave_form.instance.staff.profile.immediate_supervisor.email],
                fail_silently=False,
            )
            messages.success(request, "Leave applied successfully. Your Immediate Supervisor will review it sortly.")
        if leave_filter.is_valid():
            if leave_filter.cleaned_data.get('employee') or leave_filter.cleaned_data.get('department') or leave_filter.cleaned_data.get('date'):
                _date = leave_filter.cleaned_data.get('date')
                if _date:
                    leave_roster = leave_roster.filter(start_date__year=_date.year, start_date__month=_date.month).all().order_by('-date_applied')
                leave_roster = leave_roster.filter(
                    staff__first_name__icontains=leave_filter.cleaned_data.get('employee'),
                    staff__profile__staff_profile__department__name__icontains=leave_filter.cleaned_data.get('department')
                ).all().order_by('-date_applied')
    paginator = Paginator(leave_roster, 10)
    try:
        leave_roster = paginator.page(page)
    except:
        leave_roster = paginator.page(1)
    return render(request, "leave_roster/leave_roster.html", {
        'leave_roster': leave_roster, 'filter_form': FilterLeaves, 'current_page': 'leave_roster', 'leave_form': LeaveApplicationForm
    })

def leave_detail(request, leave_id):
    leave = LeaveRoster.objects.filter(id=leave_id).first()
    if leave:
        staff = Employee.objects.filter(staff_id=leave.staff.profile.staff_profile.staff_id)
        if not staff:
            messages.error(request, "No recognize staff is associated with that leave.")
            return HttpResponseRedirect(reverse('leave_roster'))
        return render(request, 'leave_roster/leave.html', {
            'leave': leave, 'staff': staff, 'current_page': 'leave_roster'
        })
    messages.error(request, "No valid leave object waas found.")
    raise HttpResponseRedirect(reverse('leave_roster'))
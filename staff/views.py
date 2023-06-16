from django.shortcuts import render
from .models import Employee
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def dashboard(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('leave_roster'))
    total_staffs = len(Employee.objects.all())
    full_time_staffs = len(Employee.objects.filter(employment_status="Full Time").all())
    part_time_staffs = len(Employee.objects.filter(employment_status="Part Time").all())
    probation = len(Employee.objects.filter(employment_status="Probation").all())
    interns = len(Employee.objects.filter(employment_status="Intern").all())
    on_leave = len(Employee.objects.filter(employment_status="On Leave").all())
    on_suspension = len(Employee.objects.filter(employment_status="On Suspension").all())
    resigned = len(Employee.objects.filter(employment_status="Resigned").all())
    fired = len(Employee.objects.filter(employment_status="Fired").all())
    temporary = len(Employee.objects.filter(employment_status="Temporary").all())
    contract = len(Employee.objects.filter(employment_status="Contract").all())
    independent_contract = len(Employee.objects.filter(employment_status="Independent Contract").all())

    staffs = Employee.objects.all().order_by("-hired_date")[:4]

    return render(request, "staff/dashboard.html",{
        'total_staffs': total_staffs, 'full_time_staffs': full_time_staffs, 'part_time_staffs': part_time_staffs, 'probation': probation,
        'interns': interns, 'on_leave': on_leave, 'on_suspension': on_suspension, 'resigned': resigned, 'fired': fired, 'temporary': temporary,
        'contract':contract, 'independent_contract': independent_contract, 'staffs': staffs, 'current_page': 'dashboard'
    })

@login_required
def staffs(request):
    staffs = Employee.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(staffs, 15)

    try:
        paginator = paginator.page(page)
    except:
        paginator = paginator.page(1)

    return render(request, "staff/staffs.html", {
        'staffs': paginator, 'current_page': 'staffs'
    })

@login_required
def staff_profile(request, staff_id):
    staff = get_object_or_404(Employee, id=staff_id)
    return render(request, "staff/profile.html",{
                    'staff': staff, 'current_page': 'staffs'
                 })
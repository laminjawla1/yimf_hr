from django.shortcuts import render
from .models import Payroll
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from staff.models import Employee
from datetime import datetime
from .forms import PayrollForm, FilterPayrollForm
import inflect

@login_required
def payrolls(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
    payrolls = Payroll.objects.filter(
        date__year=timezone.now().year, date__month=timezone.now().month
    ).order_by('-net_pay')
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        filter_form = FilterPayrollForm(request.POST)
        if form.is_valid():
            form.instance.staff_id = form.instance.employee.staff_id
            form.instance.basic_salary = round(form.instance.basic_salary, 4)
            form.instance.medical_allowance = round(form.instance.basic_salary * 0.1666666667, 4)
            form.instance.transport_allowance = round(form.instance.basic_salary * 0.2333333333, 4)
            form.instance.responsibility_allowance = round(form.instance.basic_salary * 0.4666666667, 4)
            form.instance.housing_allowance =round( form.instance.basic_salary * 0.1333333333, 4)
            form.instance.gross_pay = round(form.instance.basic_salary + form.instance.medical_allowance + form.instance.transport_allowance + form.instance.responsibility_allowance + form.instance.housing_allowance + form.instance.risk_allowance, 2)
            if form.instance.basic_salary > 2000:
                form.instance.income_tax = round(((((form.instance.gross_pay * 12) - 64000) * (25 / 100)) + 5000) / 12, 4)

            form.instance.sshfc = round((10 / 100) * form.instance.basic_salary, 4)
            form.instance.individual_sshfc = round((5 / 100) * form.instance.basic_salary, 4)
            form.instance.individual_sshfc = round((5 / 100) * form.instance.basic_salary, 4)
            form.instance.net_pay = round(form.instance.gross_pay - form.instance.income_tax - form.instance.individual_sshfc - form.instance.deduction - form.instance.staff_fin, 4)
            form.save()
            messages.success(request, "Payroll added successfully 😊")
        if filter_form.is_valid():
            if filter_form.cleaned_data.get('staff') or filter_form.cleaned_data.get('staff_id') or filter_form.cleaned_data.get('date'):
                _date = filter_form.cleaned_data.get('date')
                if _date:
                    payrolls = Payroll.objects.filter(date__year=_date.year, date__month=_date.month).all()
                payrolls = payrolls.filter(employee__employee_name__icontains=filter_form.cleaned_data.get('staff'),
                                                    employee__staff_id__icontains=filter_form.cleaned_data.get('staff_id')).all()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(payrolls, 8)

    basic_total = payrolls.aggregate(Sum('basic_salary')).get('basic_salary__sum') or 0
    medical_total = payrolls.aggregate(Sum('medical_allowance')).get('medical_allowance__sum') or 0
    transport_total = payrolls.aggregate(Sum('transport_allowance')).get('transport_allowance__sum') or 0
    responsibility_total = payrolls.aggregate(Sum('responsibility_allowance')).get('responsibility_allowance__sum') or 0
    housing_total = payrolls.aggregate(Sum('housing_allowance')).get('housing_allowance__sum') or 0
    gross_total = payrolls.aggregate(Sum('gross_pay')).get('gross_pay__sum') or 0
    income_total = payrolls.aggregate(Sum('income_tax')).get('income_tax__sum') or 0
    sshfc_total = payrolls.aggregate(Sum('sshfc')).get('sshfc__sum') or 0
    individual_sshfc_total = payrolls.aggregate(Sum('individual_sshfc')).get('individual_sshfc__sum') or 0
    deduction_total = payrolls.aggregate(Sum('deduction')).get('deduction__sum') or 0
    icf_total = payrolls.aggregate(Sum('icf')).get('icf__sum') or 0
    net_total = payrolls.aggregate(Sum('net_pay')).get('net_pay__sum') or 0
    staff_fin = payrolls.aggregate(Sum('staff_fin')).get('staff_fin__sum') or 0
    absolute_total = basic_total + medical_total + transport_total + responsibility_total + housing_total + gross_total \
                    + income_total + sshfc_total + individual_sshfc_total + deduction_total + icf_total + net_total

    try:
        paginator = paginator.page(page)
    except:
        paginator = paginator.page(1)

    return render(request, "payroll/payrolls.html", {
        'payrolls': paginator, 'basic_total': basic_total, 'medical_total': medical_total, 'transport_total': transport_total,
        'responsibility_total': responsibility_total, 'housing_total': housing_total, 'gross_total': gross_total, 'income_total': income_total,
        'sshfc_total': sshfc_total, 'individual_sshfc_total': individual_sshfc_total, 'deduction_total': deduction_total, 'icf_total': icf_total,
        'net_total': net_total, 'absolute_total': absolute_total, 'staff_fin_total': staff_fin,
        'current_page': 'payrolls', 'form': PayrollForm, 'legend': 'Add Payroll', 'button': 'Add', 'filter_form': FilterPayrollForm,
    })

class UpdatePayrollView(LoginRequiredMixin, UpdateView):
    model = Payroll
    fields = ['employee', 'basic_salary', 'income_tax', 'staff_fin', 'deduction', 'deduction_type']

    def form_valid(self, form):
        form.instance.staff_id = form.instance.employee.staff_id
        form.instance.basic_salary = round(form.instance.basic_salary, 4)
        form.instance.medical_allowance = round(form.instance.basic_salary * 0.1666666667, 4)
        form.instance.transport_allowance = round(form.instance.basic_salary * 0.2333333333, 4)
        form.instance.responsibility_allowance = round(form.instance.basic_salary * 0.4666666667, 4)
        form.instance.housing_allowance =round( form.instance.basic_salary * 0.1333333333, 4)
        form.instance.gross_pay = round(form.instance.basic_salary + form.instance.medical_allowance + form.instance.transport_allowance + form.instance.responsibility_allowance + form.instance.housing_allowance, 4)
        if form.instance.basic_salary > 2000:
            form.instance.income_tax = round(((((form.instance.gross_pay * 12) - 64000) * (25 / 100)) + 5000) / 12, 4)
        form.instance.sshfc = round((10 / 100) * form.instance.basic_salary, 4)
        form.instance.individual_sshfc = round((5 / 100) * form.instance.basic_salary, 4)
        form.instance.individual_sshfc = round((5 / 100) * form.instance.basic_salary, 4)
        form.instance.net_pay = round(form.instance.gross_pay - form.instance.income_tax - form.instance.individual_sshfc - form.instance.deduction - form.instance.staff_fin, 4)
        messages.success(self.request, "Payroll updated successfully.")
        return super().form_valid(form)
    
    def get_context_data(self, *args, **kwargs):
        context = super(UpdatePayrollView, self).get_context_data(*args, **kwargs)
        context['button'] = 'Update'
        context['legend'] = 'Update Payroll'
        context['current_page'] = 'payrolls'
        return context

@login_required
def staff_payslip(request):
    if request.method == 'POST':
        employee = request.POST['employee']
        date = request.POST['date']
        staff_id = request.POST['staff_id']

        if not employee and not date and not staff_id:
            messages.error(request, 'Enter some query parameters')
            return HttpResponseRedirect(reverse('payrolls'))

        if employee and not date and not staff_id:
            messages.error(request, 'Specify the staff id too')
            return HttpResponseRedirect(reverse('payrolls'))
        payslip = None
        if date and staff_id and employee:
            try:
                date = date.split('-')
            except:
                messages.error(request, 'Invalid date format')
                return HttpResponseRedirect(reverse('payrolls'))
            try:
                _date = datetime(int(date[0]), int(date[1]), int(date[2]))
            except:
                messages.error(request, 'Invalid date format')
                return HttpResponseRedirect(reverse('payrolls'))
            
            payslip = Payroll.objects.filter(
                        employee__employee_name=employee, employee__staff_id=staff_id,
                        date__year=_date.year, date__month=_date.month).first()
        elif staff_id and employee:
            payslip = Payroll.objects.filter(
                        employee__staff_id=staff_id,
                        date__year=timezone.now().year, date__month=timezone.now().month).first()
        elif staff_id and date:
            try:
                date = date.split('-')
            except:
                messages.error(request, 'Invalid date format')
                return HttpResponseRedirect(reverse('payrolls'))
            try:
                _date = datetime(int(date[0]), int(date[1]), int(date[2]))
            except:
                messages.error(request, 'Invalid date format')
                return HttpResponseRedirect(reverse('payrolls'))
            
            payslip = Payroll.objects.filter(
                        employee__staff_id=staff_id,
                        date__year=_date.year, date__month=_date.month).first()
        elif staff_id:
            payslip = Payroll.objects.filter(
                        employee__staff_id=staff_id,
                        date__year=timezone.now().year, date__month=timezone.now().month).first()
        if payslip:
            staff = Employee.objects.filter(employee_name=employee).first()
            if not staff:
                staff = Employee.objects.filter(staff_id=staff_id).first()
                if not staff:
                    messages.error(request, 'No recognize staff is associated with that payslip')
                    return HttpResponseRedirect(reverse('payrolls'))
            net_pay_in_words = inflect.engine()
            net_pay_in_words = net_pay_in_words.number_to_words(int(payslip.net_pay)).capitalize() + " dalasis"
            total_deduction = payslip.icf + payslip.individual_sshfc + payslip.income_tax + payslip.staff_fin + payslip.deduction
            return render(request, 'payroll/payslip.html', {
                'payslip': payslip, 'staff': staff, 'net_pay_in_words': net_pay_in_words, 'total_deduction': total_deduction,
                'current_page': 'payrolls'
            })
        messages.error(request, 'The requested payroll is not available')
        return HttpResponseRedirect(reverse('payrolls'))
    else:
        return HttpResponseRedirect(reverse('payrolls'))

def render_payslip(request, payroll_id):
    payslip = Payroll.objects.filter(id=payroll_id).first()
    if payslip:
        staff = Employee.objects.filter(staff_id=payslip.employee.staff_id).first()
        if not staff:
                messages.error(request, 'No recognize staff is associated with that payslip')
                return HttpResponseRedirect(reverse('payrolls'))
        net_pay_in_words = inflect.engine()
        net_pay_in_words = net_pay_in_words.number_to_words(int(payslip.net_pay)).capitalize() + " dalasis"
        total_deduction = payslip.icf + payslip.individual_sshfc + payslip.income_tax + payslip.staff_fin + payslip.deduction
        return render(request, 'payroll/payslip.html', {
            'payslip': payslip, 'staff': staff, 'net_pay_in_words': net_pay_in_words, 'total_deduction': total_deduction,
            'current_page': 'payrolls'
        })
    else:
        messages.error(request, 'The requested payroll is not available')
        return HttpResponseRedirect(reverse('payrolls'))
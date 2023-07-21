import csv
from datetime import datetime

import inflect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import UpdateView
from staff.models import Employee

from .forms import FilterPayrollForm, PayrollForm
from .models import Payroll


@login_required
def payrolls(request):
    payrolls = Payroll.objects.filter(
        date__year=timezone.now().year, date__month=timezone.now().month
    ).order_by('-net_pay')
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        payrolls = Paginator(payrolls, 8)
        try:
            payrolls = payrolls.page(page)
        except:
            payrolls = payrolls.page(1)
    if request.method == 'POST':
        if request.POST.get('from_date') and request.POST.get('to_date'):
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            items = Payroll.objects.filter(
                date__gte=datetime.strptime(from_date, '%Y-%m-%d'),
                date__lte=datetime.strptime(to_date, '%Y-%m-%d'),
            ).order_by('date')
            if not items:
                messages.error(request, "No payroll is available for download")
                return HttpResponseRedirect(reverse("payrolls"))
            headers = ["EMPLOYEE", "BASIC SALARY", "MEDICAL ALLOWANCE", "TRANSPORT ALLOWANCE", "RESPONSIBILITY ALLOWANCE",
                       "HOUSING ALLOWANCE", "RISK ALLOWANCE", "SSHFC", "INDIVIDUAL SSHFC", "ICF", "INCOME TAX", "DEDUCTION",
                       "DEDUCTION TYPE", "STAFF FINANCING", "GROSS PAY", "NET PAY", "REFUND", "DATE"
            ]
            
            response = HttpResponse(
                content_type='text/csv',
                headers = {'Content-Disposition': f'attachment; filename="yimf_payroll_{from_date}_to_{to_date}.csv"'},
            )
            writer = csv.writer(response)
            writer.writerow([f"YONNA ISLAMIC MICROFINANCE PAYROLL - {from_date} TO {to_date}"])
            writer.writerow(headers)
            for w in items:
                writer.writerow([w.employee.employee_name, w.basic_salary, w.medical_allowance, w.transport_allowance,
                                w.responsibility_allowance, w.housing_allowance, w.risk_allowance, w.sshfc,
                                w.individual_sshfc, w.icf, w.income_tax, w.deduction, w.deduction_type,
                                w.staff_fin, w.gross_pay, w.net_pay, w.refund, w.date.strftime("%Y-%m-%d")])
            return response
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
            form.instance.net_pay = round(form.instance.gross_pay - form.instance.income_tax - form.instance.individual_sshfc - form.instance.deduction - form.instance.staff_fin + form.instance.refund, 4)
            form.save()
            messages.success(request, "Payroll added successfully 😊")
        if filter_form.is_valid():
            if filter_form.cleaned_data.get('staff') or filter_form.cleaned_data.get('staff_id') or filter_form.cleaned_data.get('date'):
                _date = filter_form.cleaned_data.get('date')
                if _date:
                    payrolls = Payroll.objects.filter(date__year=_date.year, date__month=_date.month).all()
                payrolls = payrolls.filter(employee__employee_name__icontains=filter_form.cleaned_data.get('staff'),
                                                    employee__staff_id__icontains=filter_form.cleaned_data.get('staff_id')).all()

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

    return render(request, "payroll/payrolls.html", {
        'payrolls': payrolls, 'basic_total': basic_total, 'medical_total': medical_total, 'transport_total': transport_total,
        'responsibility_total': responsibility_total, 'housing_total': housing_total, 'gross_total': gross_total, 'income_total': income_total,
        'sshfc_total': sshfc_total, 'individual_sshfc_total': individual_sshfc_total, 'deduction_total': deduction_total, 'icf_total': icf_total,
        'net_total': net_total, 'absolute_total': absolute_total, 'staff_fin_total': staff_fin,
        'current_page': 'payrolls', 'form': PayrollForm, 'legend': 'Add Payroll', 'button': 'Add', 'filter_form': FilterPayrollForm,
    })

class UpdatePayrollView(LoginRequiredMixin, UpdateView):
    model = Payroll
    fields = ['employee', 'risk_allowance', 'basic_salary', 'income_tax', 'staff_fin', 'deduction', 'refund', 'deduction_type']

    def form_valid(self, form):
        form.instance.staff_id = form.instance.employee.staff_id
        form.instance.basic_salary = round(form.instance.basic_salary, 4)
        form.instance.medical_allowance = round(form.instance.basic_salary * 0.1666666667, 4)
        form.instance.transport_allowance = round(form.instance.basic_salary * 0.2333333333, 4)
        form.instance.responsibility_allowance = round(form.instance.basic_salary * 0.4666666667, 4)
        form.instance.housing_allowance =round( form.instance.basic_salary * 0.1333333333, 4)
        form.instance.gross_pay = round(form.instance.basic_salary + form.instance.medical_allowance + form.instance.transport_allowance + form.instance.responsibility_allowance + form.instance.housing_allowance + form.instance.risk_allowance, 4)
        if form.instance.basic_salary > 2000:
            form.instance.income_tax = round(((((form.instance.gross_pay * 12) - 64000) * (25 / 100)) + 5000) / 12, 4)
        form.instance.sshfc = round((10 / 100) * form.instance.basic_salary, 4)
        form.instance.individual_sshfc = round((5 / 100) * form.instance.basic_salary, 4)
        form.instance.individual_sshfc = round((5 / 100) * form.instance.basic_salary, 4)
        form.instance.net_pay = round(form.instance.gross_pay - form.instance.income_tax - form.instance.individual_sshfc - form.instance.deduction - form.instance.staff_fin + form.instance.refund, 4)
        messages.success(self.request, "Payroll updated successfully.")
        return super().form_valid(form)
    
    def get_context_data(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionDenied()
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
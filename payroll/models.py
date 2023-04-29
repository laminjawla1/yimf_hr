from django.db import models
from staff.models import Employee
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator


class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    basic_salary = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    medical_allowance = models.FloatField(default=0.0)
    transport_allowance = models.FloatField(default=0.0)
    responsibility_allowance = models.FloatField(default=0.0)
    housing_allowance = models.FloatField(default=0.0)
    gross_pay = models.FloatField(default=0.0)
    income_tax = models.FloatField(default=0.0)
    sshfc = models.FloatField(default=0.0)
    individual_sshfc =  models.FloatField(default=0.0)
    deduction = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    staff_fin = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    icf = models.FloatField(default=15)
    net_pay = models.FloatField(default=0.0)
    deduction_type = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(null=False, default=timezone.now)
    staff_id = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.employee.employee_name
    
    def get_absolute_url(self):
        return reverse('payrolls')
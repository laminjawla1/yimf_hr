from django.urls import path
from .views import payrolls, UpdatePayrollView, staff_payslip, render_payslip

urlpatterns = [
    path("staff_payroll/", payrolls, name="payrolls"),
    path("staff_payslip", staff_payslip, name="staff_payslip"),
    path("<int:payroll_id>/current_month/view", render_payslip, name="render_payslip"),
    path("<int:pk>/update", UpdatePayrollView.as_view(), name="update_payroll"),
]
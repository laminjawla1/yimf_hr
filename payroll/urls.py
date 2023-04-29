from django.urls import path
from .views import payrolls, AddPayrollView, UpdatePayrollView, staff_payslip, render_payslip, download_payslip

urlpatterns = [
    path("staff_payroll/", payrolls, name="payrolls"),
    path("staff_payslip", staff_payslip, name="staff_payslip"),
    path("<int:payroll_id>/current_month/view", render_payslip, name="render_payslip"),
    path("<int:payroll_id>/download/", download_payslip, name="download_payslip"),
    path("add_payroll/", AddPayrollView.as_view(), name="add_payroll"),
    path("<int:pk>/update", UpdatePayrollView.as_view(), name="update_payroll"),
]
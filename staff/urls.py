from django.urls import path
from .views import dashboard, staffs, staff_profile

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("employee_list", staffs, name="staffs"),
    path("staff_profile/view", staff_profile, name="staff_profile")
]
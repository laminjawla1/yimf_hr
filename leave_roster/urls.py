from django.urls import path

from . import views

urlpatterns = [
    path("", views.leave_roster, name="leave_roster"),
    path("leave/<int:leave_id>/detail", views.leave_detail, name="leave_detail"),
    path("leave/<int:pk>/update", views.UpdateLeave.as_view(), name="apply_leave"),
]
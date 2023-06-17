from django.db import models
from staff.models import Employee
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class LeaveRoster(models.Model):
    # Staff Details
    staff = models.ForeignKey(User, on_delete=models.CASCADE)

    # Leave Details
    type_of_leave = models.CharField(max_length=50, choices=[
        ('Annual', 'Annual'),
        ('Maternity', 'Maternity'),
        ('Sick', 'Sick'),
        ('Compassionate', 'Compassionate'),
    ])
    leave_reason = models.TextField()

    # Leave Dates
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    number_of_days = models.IntegerField()

    status = models.TextField(choices=[
        ('Applicant', 'Applicant'),
        ('Immediate Supervisor', 'Immediate Supervisor'),
        ('Head Of Department', 'Head Of Department'),
        ('Rejected', 'Rejected'),
        ('Approved', 'Approved'),
        ('HR Office', 'HR Office'),
    ])
    approved = models.BooleanField(default=False)
    date_applied = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.staff.first_name} {self.staff.last_name}"
    
    def get_absolute_url(self):
        return reverse('leave_roster')

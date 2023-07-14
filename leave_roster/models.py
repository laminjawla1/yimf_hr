from django.db import models
from staff.models import Employee
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class LeaveRoster(models.Model):
    # Staff Details
    staff = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)

    # Leave Details
    type_of_leave = models.CharField(max_length=50, choices=[
        ('Annual', 'Annual'),
        ('Maternity', 'Maternity'),
        ('Paternity', 'Paternity'),
        ('Sick', 'Sick'),
        ('Compassionate', 'Compassionate'),
    ])
    leave_reason = models.TextField()

    # Leave Dates
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    number_of_days = models.IntegerField()

    status = models.TextField(null=True, blank=True, choices=[('Approved', 'Approved')])
    date_applied = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.staff}"
    
    def get_absolute_url(self):
        return reverse('leave_roster')

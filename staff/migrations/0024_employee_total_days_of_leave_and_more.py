# Generated by Django 4.2 on 2023-05-31 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0023_employee_suspensions"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="total_days_of_leave",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="employee",
            name="total_leave_balance",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="employee",
            name="total_leave_days_taken",
            field=models.IntegerField(default=0),
        ),
    ]
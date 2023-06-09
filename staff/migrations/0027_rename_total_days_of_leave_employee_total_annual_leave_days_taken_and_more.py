# Generated by Django 4.2 on 2023-06-17 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0026_alter_employee_country"),
    ]

    operations = [
        migrations.RenameField(
            model_name="employee",
            old_name="total_days_of_leave",
            new_name="total_annual_leave_days_taken",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="total_leave_days_taken",
        ),
        migrations.AddField(
            model_name="employee",
            name="total_days_of_leave_taken",
            field=models.IntegerField(default=0, editable=False),
        ),
    ]

# Generated by Django 4.2 on 2023-06-07 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0024_employee_total_days_of_leave_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="country",
            field=models.CharField(blank=True, choices=[], max_length=100, null=True),
        ),
    ]

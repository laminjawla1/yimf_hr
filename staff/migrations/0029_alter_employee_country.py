# Generated by Django 4.2 on 2023-07-19 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0028_alter_employee_total_days_of_leave_taken"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

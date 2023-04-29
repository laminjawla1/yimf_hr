# Generated by Django 4.2 on 2023-04-27 17:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payroll", "0004_alter_payroll_basic_salary_alter_payroll_deduction_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="payroll",
            name="staff_fin",
            field=models.FloatField(
                default=0.0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
    ]

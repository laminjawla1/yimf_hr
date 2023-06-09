# Generated by Django 4.2 on 2023-04-26 07:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payroll", "0003_payroll_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payroll",
            name="basic_salary",
            field=models.FloatField(
                default=0.0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="payroll",
            name="deduction",
            field=models.FloatField(
                default=0.0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="payroll",
            name="icf",
            field=models.FloatField(default=15),
        ),
    ]

# Generated by Django 4.2 on 2023-04-25 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("staff", "0020_remove_employee_division"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payroll",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("basic_salary", models.FloatField()),
                ("medical_allowance", models.FloatField()),
                ("transport_allowance", models.FloatField()),
                ("responsibility_allowance", models.FloatField()),
                ("housing_allowance", models.FloatField()),
                ("gross_pay", models.FloatField()),
                ("income_tax", models.FloatField()),
                ("sshfc", models.FloatField()),
                ("individual_sshfc", models.FloatField()),
                ("deduction", models.FloatField(default=0.0)),
                ("icf", models.FloatField(default=0.0)),
                ("net_pay", models.FloatField()),
                ("comment", models.TextField(blank=True, null=True)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="staff.employee"
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 4.2 on 2023-05-02 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payroll", "0007_payroll_staff_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payroll",
            name="income_tax",
            field=models.FloatField(default=0.0, null=True),
        ),
    ]

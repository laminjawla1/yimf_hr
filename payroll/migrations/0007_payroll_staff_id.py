# Generated by Django 4.2 on 2023-04-29 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payroll", "0006_remove_payroll_comment_payroll_deduction_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="payroll",
            name="staff_id",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
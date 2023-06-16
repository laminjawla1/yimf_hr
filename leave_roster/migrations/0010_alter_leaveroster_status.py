# Generated by Django 4.2 on 2023-06-16 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leave_roster", "0009_leaveroster_date_applied"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leaveroster",
            name="status",
            field=models.TextField(
                choices=[
                    ("Applicant", "Applicant"),
                    ("Immediate Supervisor", "Immediate Supervisor"),
                    ("Head Of Department", "Head Of Department"),
                    ("Rejected", "Rejected"),
                    ("Approved", "Approved"),
                    ("Pending", "Pending"),
                ]
            ),
        ),
    ]
# Generated by Django 4.2 on 2023-06-13 17:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("leave_roster", "0008_remove_leaveroster_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="leaveroster",
            name="date_applied",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

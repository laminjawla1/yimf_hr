# Generated by Django 4.2 on 2023-04-20 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0020_remove_employee_division"),
        ("section", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Division",
        ),
    ]

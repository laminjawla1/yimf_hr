# Generated by Django 4.2 on 2023-06-15 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_alter_profile_head_of_department_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="is_hod",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="is_supervisor",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]

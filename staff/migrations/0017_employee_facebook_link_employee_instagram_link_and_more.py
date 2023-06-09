# Generated by Django 4.2 on 2023-04-18 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0016_employee_warning"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="facebook_link",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="instagram_link",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="linkedin_link",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="twitter_link",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

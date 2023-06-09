# Generated by Django 4.2 on 2023-04-14 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0007_alter_employee_emp_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="emp_status",
            field=models.CharField(
                choices=[
                    ("Attachment", "Attachment"),
                    ("Contract", "Contract"),
                    ("Full Time", "Full Time"),
                    ("Independent Contract", "Independent Contract"),
                    ("Intern", "Intern"),
                    ("Part Time", "Part Time"),
                    ("Temporary", "Temporary"),
                ],
                max_length=50,
            ),
        ),
    ]

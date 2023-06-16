# Generated by Django 4.2 on 2023-05-31 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leave_roster", "0002_leaveroster_email_leaveroster_end_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leaveroster",
            name="home_tel",
            field=models.CharField(default="", max_length=14),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="leaveroster",
            name="leave_reason",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="leaveroster",
            name="mobile_tel",
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name="leaveroster",
            name="number_of_days",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="leaveroster",
            name="type_of_leave",
            field=models.CharField(
                choices=[
                    ("Annual", "Annual"),
                    ("Maternity", "Maternity"),
                    ("Sick", "Sick"),
                    ("Compassionate", "Compassionate"),
                ],
                max_length=50,
            ),
        ),
    ]
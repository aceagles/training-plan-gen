# Generated by Django 3.2.5 on 2022-01-14 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plan_generator", "0002_rename_disance_day_distance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="day",
            name="time",
            field=models.DurationField(),
        ),
    ]

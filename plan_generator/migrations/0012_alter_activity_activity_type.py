# Generated by Django 3.2.5 on 2022-06-25 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plan_generator", "0011_alter_day_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="activity_type",
            field=models.CharField(
                choices=[("RUN", "Run"), ("RIDE", "Ride"), ("WALK", "Walk")],
                default="RUN",
                max_length=30,
            ),
        ),
    ]

# Generated by Django 3.2.5 on 2022-06-26 10:34

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plan_generator", "0015_auto_20220626_0935"),
    ]

    operations = [
        migrations.AlterField(
            model_name="day",
            name="ascent",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="day",
            name="distance",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="day",
            name="plan_distance",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="day",
            name="plan_time",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="day",
            name="time",
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]

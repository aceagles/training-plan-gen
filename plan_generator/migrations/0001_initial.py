# Generated by Django 3.2.5 on 2022-01-14 21:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField()),
                ("duration", models.DurationField()),
                ("distance", models.FloatField()),
                ("ascent", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="TrainingPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_volume", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Week",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="StravaActivity",
            fields=[
                (
                    "activity_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="plan_generator.activity",
                    ),
                ),
                ("url", models.URLField()),
            ],
            bases=("plan_generator.activity",),
        ),
        migrations.CreateModel(
            name="Day",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("plan_distance", models.FloatField()),
                ("plan_time", models.FloatField()),
                ("disance", models.FloatField()),
                ("time", models.FloatField()),
                ("ascent", models.FloatField()),
                (
                    "week",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="days",
                        to="plan_generator.week",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="activity",
            name="day",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="activities",
                to="plan_generator.day",
            ),
        ),
    ]

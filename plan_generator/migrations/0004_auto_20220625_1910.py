# Generated by Django 3.2.5 on 2022-06-25 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
        ("plan_generator", "0003_alter_day_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="activity",
            name="profile",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="account.profile",
            ),
        ),
        migrations.DeleteModel(
            name="StravaActivity",
        ),
    ]

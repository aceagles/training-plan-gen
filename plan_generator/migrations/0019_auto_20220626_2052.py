# Generated by Django 3.2.5 on 2022-06-26 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_generator', '0018_alter_activity_activity_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='distance',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='week',
            name='plan_distance',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='week',
            name='plan_time',
            field=models.DurationField(default=0),
        ),
        migrations.AlterField(
            model_name='week',
            name='time',
            field=models.DurationField(default=0),
        ),
    ]
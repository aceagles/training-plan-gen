# Generated by Django 3.2.5 on 2022-06-25 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_generator', '0007_auto_20220625_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]

# Generated by Django 3.2.5 on 2022-06-26 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='access_token',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='expires_at',
            field=models.PositiveBigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='refresh_token',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

# Generated by Django 3.0.2 on 2020-07-11 07:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cab', '0003_auto_20200711_0643'),
    ]

    operations = [
        migrations.AddField(
            model_name='caborder',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='caborder',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 11, 7, 22, 7, 9407, tzinfo=utc)),
        ),
    ]
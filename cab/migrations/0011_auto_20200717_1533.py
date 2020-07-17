# Generated by Django 3.0.2 on 2020-07-17 10:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cab', '0010_auto_20200717_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabdetails',
            name='rating',
            field=models.FloatField(default=1, max_length=10),
        ),
        migrations.AlterField(
            model_name='caborder',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 17, 10, 3, 52, 404932, tzinfo=utc)),
        ),
    ]

# Generated by Django 3.0.2 on 2020-08-01 19:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cab', '0021_auto_20200731_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caborder',
            name='pickupTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 1, 19, 24, 39, 274559, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='caborder',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 1, 19, 24, 39, 274526, tzinfo=utc)),
        ),
    ]
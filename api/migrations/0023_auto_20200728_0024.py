# Generated by Django 3.0.2 on 2020-07-27 18:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20200726_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complain',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 27, 18, 54, 58, 133136, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 27, 18, 54, 58, 132533, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='pickupDate',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 27, 18, 54, 58, 128280, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 27, 18, 54, 58, 128251, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='productcomplain',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 27, 18, 54, 58, 131793, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storerestro',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 27, 18, 54, 58, 131201, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tax',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 27, 18, 54, 58, 133797, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 27, 18, 54, 58, 129161, tzinfo=utc)),
        ),
    ]

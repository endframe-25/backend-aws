# Generated by Django 3.0.2 on 2020-07-26 14:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20200724_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='review',
            field=models.CharField(default='NA', max_length=256),
        ),
        migrations.AddField(
            model_name='order',
            name='reviewState',
            field=models.IntegerField(default=-1, max_length=256),
        ),
        migrations.AlterField(
            model_name='complain',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 14, 52, 59, 854527, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 14, 52, 59, 853933, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='pickupDate',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 14, 52, 59, 849853, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 14, 52, 59, 849822, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='productcomplain',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 14, 52, 59, 853301, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storerestro',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 14, 52, 59, 852732, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tax',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 14, 52, 59, 855161, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 14, 52, 59, 850752, tzinfo=utc)),
        ),
    ]

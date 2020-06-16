# Generated by Django 3.0.2 on 2020-06-16 13:15

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200616_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complain',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 13, 15, 16, 436200, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 13, 15, 16, 435614, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 13, 15, 16, 433908, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storerestro',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 13, 15, 16, 434963, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tax',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 13, 15, 16, 436782, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='services',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.cat'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 13, 15, 16, 431889, tzinfo=utc)),
        ),
    ]

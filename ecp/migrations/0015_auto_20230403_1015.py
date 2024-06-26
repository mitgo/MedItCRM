# Generated by Django 3.2.17 on 2023-04-03 01:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ecp', '0014_auto_20230403_1015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decrees',
            name='date',
        ),
        migrations.AddField(
            model_name='decrees',
            name='d_date',
            field=models.DateField(default=datetime.datetime(2023, 4, 3, 1, 15, 30, 626253, tzinfo=utc), verbose_name='Дата договора'),
        ),
        migrations.AlterField(
            model_name='esigns',
            name='date_start',
            field=models.DateField(default=datetime.datetime(2023, 4, 3, 1, 15, 30, 633322, tzinfo=utc), verbose_name='Дата подачи заявки'),
        ),
    ]

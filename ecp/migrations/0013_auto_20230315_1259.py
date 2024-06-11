# Generated by Django 3.2.17 on 2023-03-15 03:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ecp', '0012_auto_20230309_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decrees',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 3, 15, 3, 59, 34, 677638, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='esigns',
            name='date_start',
            field=models.DateField(default=datetime.datetime(2023, 3, 15, 3, 59, 34, 682643, tzinfo=utc), verbose_name='Дата подачи заявки'),
        ),
        migrations.AlterField(
            model_name='persons',
            name='decrees',
            field=models.ManyToManyField(blank=True, null=True, to='ecp.Decrees', verbose_name='Приказы'),
        ),
    ]

# Generated by Django 4.2.1 on 2023-10-31 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecp', '0041_esignstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esignstatus',
            name='date',
            field=models.DateTimeField(verbose_name='Дата установления статуса'),
        ),
    ]

# Generated by Django 4.2.1 on 2023-10-03 02:27

import django.core.validators
from django.db import migrations, models
import ecp.models


class Migration(migrations.Migration):

    dependencies = [
        ('ecp', '0037_alter_departmenttypes_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esigns',
            name='cert',
            field=models.FileField(blank=True, null=True, upload_to=ecp.models.Esigns.get_translitfilename, validators=[django.core.validators.FileExtensionValidator(['pfx', 'rar'])], verbose_name='Файл сертификата'),
        ),
    ]

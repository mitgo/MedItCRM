# Generated by Django 4.2.1 on 2023-06-30 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecp', '0034_esigns_date_prompt_esigns_date_request_esigns_note_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='esigns',
            name='installed',
            field=models.BooleanField(default=False, verbose_name='Отметка об установке пользователю'),
        ),
    ]

# Generated by Django 3.2.17 on 2023-02-21 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainmenu',
            name='app_url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
# Generated by Django 3.2.17 on 2023-02-21 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20230221_1709'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mainmenu',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='mainmenu',
            name='parent',
        ),
    ]

# Generated by Django 3.2.17 on 2023-02-21 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_mainmenu_asdf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainmenu',
            name='level',
        ),
        migrations.RemoveField(
            model_name='mainmenu',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='mainmenu',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='mainmenu',
            name='tree_id',
        ),
    ]

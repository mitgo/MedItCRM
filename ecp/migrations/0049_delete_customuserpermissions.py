# Generated by Django 4.2.1 on 2024-03-06 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecp', '0048_customuserpermissions'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUserPermissions',
        ),
    ]
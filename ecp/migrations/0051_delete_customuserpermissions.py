# Generated by Django 4.2.1 on 2024-03-13 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecp', '0050_customuserpermissions'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUserPermissions',
        ),
    ]
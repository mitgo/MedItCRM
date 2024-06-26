# Generated by Django 3.2.17 on 2023-02-21 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_mainmenu_app_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainmenu',
            name='app_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mainmenu',
            name='root',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.mainmenu'),
        ),
    ]

# Generated by Django 4.2.1 on 2023-06-13 01:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecp', '0017_auto_20230406_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='persons',
            name='inn',
            field=models.CharField(default=28, max_length=12, verbose_name='ИНН'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='decrees',
            name='d_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата приказа'),
        ),
        migrations.AlterField(
            model_name='esigns',
            name='date_start',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата подачи заявки'),
        ),
        migrations.AlterField(
            model_name='persons',
            name='decrees',
            field=models.ManyToManyField(blank=True, null=True, related_name='persons', to='ecp.decrees', verbose_name='Приказы'),
        ),
    ]
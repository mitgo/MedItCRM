# Generated by Django 3.2.17 on 2023-02-21 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20230221_1414'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mainmenu',
            options={'ordering': ('position', 'root__position'), 'verbose_name': 'Пункт меню', 'verbose_name_plural': 'Пункты меню'},
        ),
        migrations.AddField(
            model_name='mainmenu',
            name='position',
            field=models.IntegerField(blank=True, null=True, verbose_name='Позиция'),
        ),
        migrations.AlterField(
            model_name='mainmenu',
            name='app_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='mainmenu',
            name='capt',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
    ]

# Generated by Django 4.2.1 on 2023-06-16 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecp', '0018_persons_inn_alter_decrees_d_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='esigns',
            name='cert',
            field=models.FileField(blank=True, null=True, upload_to='static/uploads/certs/%Y/%m', verbose_name='Файл сертификата'),
        ),
        migrations.AddField(
            model_name='esigns',
            name='request_link',
            field=models.CharField(default=None, max_length=255, verbose_name='Ссылка на черновик'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='esigns',
            name='request_num',
            field=models.CharField(default=None, max_length=6, verbose_name='Номер запроса'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='decrees',
            name='file',
            field=models.FileField(upload_to='static/uploads/decrees/', verbose_name='Файл приказа'),
        ),
        migrations.AlterField(
            model_name='persons',
            name='bitrh_place',
            field=models.CharField(max_length=100, verbose_name='Место рождения'),
        ),
        migrations.AlterField(
            model_name='persons',
            name='pasp_dep',
            field=models.CharField(max_length=7, verbose_name='Код подразделения'),
        ),
        migrations.AlterField(
            model_name='persons',
            name='pasp_n',
            field=models.CharField(max_length=7, verbose_name='Номер паспорта'),
        ),
        migrations.AlterField(
            model_name='persons',
            name='pasp_s',
            field=models.CharField(max_length=5, verbose_name='Серия паспорта'),
        ),
        migrations.AlterField(
            model_name='persons',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Телефон для связи'),
        ),
        migrations.AlterField(
            model_name='persons',
            name='snils',
            field=models.CharField(max_length=11, verbose_name='СНИЛС'),
        ),
    ]

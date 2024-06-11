# Generated by Django 3.2.17 on 2023-02-07 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fam', models.CharField(max_length=40)),
                ('im', models.CharField(max_length=40)),
                ('ot', models.CharField(max_length=40)),
                ('db', models.DateField()),
                ('bitrh_place', models.CharField(max_length=50)),
                ('post', models.CharField(max_length=255)),
                ('dep', models.CharField(max_length=255)),
                ('snils', models.CharField(max_length=14)),
                ('pasp_s', models.CharField(max_length=10)),
                ('pasp_n', models.CharField(max_length=10)),
                ('pasp_dep', models.CharField(max_length=10)),
                ('pasp_date', models.DateField()),
                ('pasp_kem', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ECP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('fk_person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecp.persons')),
            ],
        ),
    ]
# Generated by Django 3.2.17 on 2023-02-22 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_mainmenu_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mainmenu',
            options={'verbose_name': 'Пункт меню', 'verbose_name_plural': 'Пункты меню'},
        ),
        migrations.RenameField(
            model_name='mainmenu',
            old_name='capt',
            new_name='title',
        ),
        migrations.AddField(
            model_name='mainmenu',
            name='level',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mainmenu',
            name='lft',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mainmenu',
            name='rght',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mainmenu',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='mainmenu',
            unique_together={('parent',)},
        ),
    ]

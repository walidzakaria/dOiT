# Generated by Django 2.1.7 on 2019-09-04 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_activity_activity_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name_plural': 'activities'},
        ),
        migrations.RenameField(
            model_name='deal',
            old_name='Employee',
            new_name='employee',
        ),
        migrations.RenameField(
            model_name='deal',
            old_name='Guest',
            new_name='guest',
        ),
    ]

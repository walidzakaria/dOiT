# Generated by Django 2.1.7 on 2019-09-27 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190927_2251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeactivity',
            name='end_hour',
        ),
        migrations.RemoveField(
            model_name='employeeactivity',
            name='start_hour',
        ),
        migrations.AlterField(
            model_name='deal',
            name='comment',
            field=models.CharField(max_length=250),
        ),
    ]

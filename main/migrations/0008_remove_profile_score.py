# Generated by Django 2.2.6 on 2019-10-16 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20191017_0048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='score',
        ),
    ]

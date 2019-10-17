# Generated by Django 2.2.6 on 2019-10-13 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_auto_20191012_0436'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchLog',
            fields=[
                ('search_log_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('search_date', models.DateTimeField(auto_now_add=True)),
                ('search_text', models.CharField(db_index=True, max_length=300)),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Activity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

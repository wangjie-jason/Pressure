# Generated by Django 3.2 on 2022-11-18 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0007_db_tasks_all_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_tasks',
            name='all_threads',
            field=models.CharField(blank=True, default=[], max_length=5000, null=True),
        ),
    ]
# Generated by Django 3.2 on 2022-11-21 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0008_db_tasks_all_threads'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_tasks',
            name='all_fail_threads',
            field=models.CharField(blank=True, default=[], max_length=5000, null=True),
        ),
    ]

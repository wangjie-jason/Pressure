# Generated by Django 3.2 on 2022-11-21 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0009_db_tasks_all_fail_threads'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_projects',
            name='variable',
            field=models.CharField(blank=True, default='[]', max_length=1000, null=True),
        ),
    ]
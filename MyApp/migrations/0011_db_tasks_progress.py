# Generated by Django 3.2 on 2022-12-07 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0010_db_projects_variable'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_tasks',
            name='progress',
            field=models.IntegerField(default=0),
        ),
    ]
# Generated by Django 3.2 on 2022-11-14 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0006_auto_20221106_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_tasks',
            name='all_times',
            field=models.CharField(blank=True, default=[], max_length=5000, null=True),
        ),
    ]

# Generated by Django 5.1 on 2024-09-23 02:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songsManager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 22, 19, 34, 48, 768214)),
        ),
    ]

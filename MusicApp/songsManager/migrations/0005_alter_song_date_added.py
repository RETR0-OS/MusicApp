# Generated by Django 5.1 on 2024-09-23 04:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songsManager', '0004_alter_song_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 22, 21, 57, 23, 845397)),
        ),
    ]
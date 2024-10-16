from django.db import models
from datetime import datetime
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
import os
# Create your models here.

class Song(models.Model):
    title = models.CharField(max_length=400)
    song_mp3 = models.FileField(upload_to="songs/")
    date_added = models.DateTimeField(default=datetime.now())
    artists = models.CharField(max_length=1000, default="Various Artists")

    def __str__(self):
        return f"{self.title} | {self.artists} | {self.date_added}"

@receiver(post_delete, sender=Song)
def delete_file_on_object_deletion(sender, instance, **kwargs):
    if instance.profile_pic:
        if os.path.isfile(instance.song_mp3.path):
            os.remove(instance.song_mp3.path)

@receiver(pre_save, sender=Song)
def delete_old_file_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_file = Song.objects.get(pk=instance.pk).song_mp3
    except Song.DoesNotExist:
        return
    new_file = instance.song_mp3
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
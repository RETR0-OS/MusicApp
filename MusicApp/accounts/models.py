from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from songsManager.models import Song
import os


usr = User.objects.get(username="r3tr0")

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="userProfilePictures/", default="defaults/default_user.svg")
    profile_pic_external = models.URLField(null=True, blank=True)
    preference_tags = models.TextField(null=True, blank=True)
    favourite_songs = models.ManyToManyField(Song, blank=True)


    def __str__(self):
        if self.user.username:
            return self.user.username
        else:
            return self.user.email

@receiver(post_delete, sender=UserProfile)
def delete_file_on_object_deletion(sender, instance, **kwargs):
    if instance.profile_pic:
        if os.path.isfile(instance.profile_pic.path):
            os.remove(instance.profile_pic.path)
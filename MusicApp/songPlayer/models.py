from django.db import models
from django.contrib.auth.models import User
from songsManager.models import Song
# Create your models here.

class UserPlaylist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_pic = models.ImageField(upload_to="playlistProfilePics/", blank=True, null=True)
    title = models.CharField(max_length=200, null=False, default="My Playlist")
    description = models.TextField(max_length=800, null=False, blank=False, default="My playlist")
    songs = models.ManyToManyField(Song, blank=True)
    is_public = models.BooleanField(default=False, null=False, editable=True)

    def __str__(self):
        return f"{self.title} | {self.user}"

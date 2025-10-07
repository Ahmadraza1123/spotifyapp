from django.db import models
from django.contrib.auth import get_user_model
from song.models import Song
from album.models import Album

User = get_user_model()

class Playlist(models.Model):
    playlist_id = models.AutoField(primary_key=True, unique=True)
    playlist_name = models.CharField(max_length=100)
    playlist_image = models.ImageField(upload_to="playlist_images/", null=True, blank=True)
    playlist_bio = models.TextField(max_length=100)
    albums = models.ManyToManyField("album.Album", blank=True, related_name="playlists")
    songs = models.ManyToManyField("song.Song", blank=True, related_name="playlists")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['playlist_name', 'created_by'],
                name='unique_playlist_per_user'
            )
        ]

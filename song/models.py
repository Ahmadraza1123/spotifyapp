from django.db import models
from album.models import Album
from django.contrib.auth import get_user_model

User = get_user_model()

class Song(models.Model):

    song_id = models.AutoField(primary_key=True)
    song_name = models.CharField(unique=True,max_length=100)
    album_name = models.ForeignKey('album.Album',on_delete=models.SET_NULL,null=True, blank=True,related_name="song")
    cover_image = models.ImageField(upload_to='song_covers/', null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="songs")
    Like = models.ManyToManyField(User, related_name='song_Like', blank=True)
    Unlike = models.ManyToManyField(User, related_name='song_Unlike', blank=True)

    def like_count(self):
        return self.Like.count()

    def unlike_count(self):
        return self.Unlike.count()






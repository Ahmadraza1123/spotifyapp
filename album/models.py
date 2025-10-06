from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='album_covers/', null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    singer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='albums_as_singer')
    album_description = models.CharField(max_length=100)
    Like = models.ManyToManyField(User,related_name='albums_Like',blank=True)
    Unlike = models.ManyToManyField(User,related_name='albums_Unlike',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return self.Like.count()

    def unlike_count(self):
        return self.Unlike.count()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['album_name', 'singer'],
                name='unique_album_per_singer'
            )
        ]



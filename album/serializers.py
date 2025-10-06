from rest_framework import serializers
from .models import Album
from song.serializers import SongSerializer


class AlbumSerializer(serializers.ModelSerializer):
    singer_name = serializers.SerializerMethodField()
    total_songs = serializers.SerializerMethodField()
    song = SongSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = [
            'album_id',
            'album_name',
            'cover_image',
            'like_count',
            'unlike_count',
            'album_description',
            'singer_name',
            'total_songs',
            'song',
            'created_at'
        ]

    def get_singer_name(self, obj):
        return obj.singer.username

    def get_total_songs(self, obj):
        return obj.song.count()

    def validate(self, data):
        request = self.context.get('request')
        user = request.user if request else None
        album_name = data.get('album_name')

        if user and Album.objects.filter(singer=user, album_name__iexact=album_name).exists():
            raise serializers.ValidationError({
                "album_name": "You already have an album with this name."
            })
        return data

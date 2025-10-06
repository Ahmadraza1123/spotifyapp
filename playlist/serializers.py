from rest_framework import serializers
from .models import Playlist


class PlaylistSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    saved_song = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = [
            'playlist_id',
            'playlist_name',
            'playlist_image',
            'playlist_bio',
            'created_at',
            'created_by',
            'saved_song',
        ]
        read_only_fields = ['created_by']


    def validate(self, data):
        user = self.context['request'].user
        playlist_name = data.get('playlist_name')

        if Playlist.objects.filter(
            created_by=user,
            playlist_name__iexact=playlist_name
        ).exists():
            raise serializers.ValidationError({
                "playlist_name": "You already have a playlist with this name."
            })
        return data

    def get_created_by(self, obj):
        return obj.created_by.username

    def get_saved_song(self, obj):
        return [
            {
                "id": song.song_id,
                "song_name": song.song_name,
                "cover_image": song.cover_image.url if song.cover_image else None,
            }
            for song in obj.songs.all()
        ]

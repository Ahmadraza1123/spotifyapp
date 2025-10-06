from rest_framework import serializers
from .models import Song
from album.models import Album


class SongSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField()
    unlike_count = serializers.ReadOnlyField()

    # album info (for output)
    album_id = serializers.IntegerField(source='album_name.album_id', read_only=True)
    album_name = serializers.CharField(source='album_name.album_name', read_only=True)
    album_singer_id = serializers.IntegerField(source='album_name.singer.id', read_only=True)
    album_singer_name = serializers.CharField(source='album_name.singer.username', read_only=True)

    # album input (for POST)
    input_album_name = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        allow_null=True
    )

    class Meta:
        model = Song
        fields = [
            'song_id',
            'song_name',
            'cover_image',
            'duration',
            'input_album_name',
            'album_id',
            'album_name',
            'album_singer_id',
            'album_singer_name',
            'like_count',
            'unlike_count'
        ]

    def validate(self, attrs):

        request = self.context['request']
        user = request.user
        album_name = attrs.pop('input_album_name', None)

        if album_name:

            album, _ = Album.objects.get_or_create(
                album_name=album_name,
                singer=user,
                defaults={'album_description': ''}
            )
            attrs['album_name'] = album
        else:

            attrs['album_name'] = None

        return attrs

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

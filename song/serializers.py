from rest_framework import serializers
from .models import Song
from album.models import Album


class SongSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField()
    unlike_count = serializers.ReadOnlyField()

    album_id = serializers.IntegerField(source="album_name.album_id", read_only=True)
    album_name = serializers.CharField(source="album_name.album_name", read_only=True)
    album_singer_id = serializers.IntegerField(source="album_name.singer.id", read_only=True)
    album_singer_name = serializers.CharField(source="album_name.singer.username", read_only=True)
    input_album_name = serializers.CharField(
        write_only=True, required=False, allow_blank=True, allow_null=True
    )

    class Meta:
        model = Song
        fields = [
            "song_id",
            "song_name",
            "cover_image",
            "duration",
            "input_album_name",
            "album_id",
            "album_name",
            "album_singer_id",
            "album_singer_name",
            "like_count",
            "unlike_count",
        ]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        album_input_name = attrs.pop("input_album_name", None)


        if getattr(user, "role", None) != "singer":
            raise serializers.ValidationError("Only singers can create songs.")

        if album_input_name:

            album_qs = Album.objects.filter(album_name=album_input_name, singer=user)

            if album_qs.exists():

                attrs["album_name"] = album_qs.first()
            else:

                if Album.objects.filter(album_name=album_input_name).exclude(singer=user).exists():
                    raise serializers.ValidationError(
                        {"input_album_name": "You cannot add a song to another singer's album."}
                    )


                album = Album.objects.create(
                    album_name=album_input_name,
                    singer=user,
                    album_description="",
                )
                attrs["album_name"] = album
        else:
            attrs["album_name"] = None

        return attrs

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

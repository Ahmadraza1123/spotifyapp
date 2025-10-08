from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Playlist
from .serializers import PlaylistSerializer
from song.models import Song
from album.models import Album


class PlaylistViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        return Playlist.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):

        if request.user.role != "normal":
            return Response(
                {"error": "Only normal users can create playlists."},
                status=status.HTTP_403_FORBIDDEN
            )


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):

         serializer.save(created_by=self.request.user)

class PlaylistViewSet(viewsets.ModelViewSet):

    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Playlist.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):

        if request.user.role != "normal":
            return Response(
                {"error": "Only normal users can create playlists."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        serializer.save(created_by=self.request.user)


class PlaylistSaveSongView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, playlist_id, song_id):
        try:

            playlist = Playlist.objects.get(playlist_id=playlist_id, created_by=request.user)
        except Playlist.DoesNotExist:
            return Response({"detail": "Playlist not found."},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            song = Song.objects.get(song_id=song_id)
        except Song.DoesNotExist:
            return Response({"detail": "Song not found."},
                            status=status.HTTP_404_NOT_FOUND)


        if song in playlist.songs.all():
            playlist.songs.remove(song)
            message = "Song removed from playlist."
        else:
            playlist.songs.add(song)
            message = "Song added to playlist."

        return Response({"detail": message}, status=status.HTTP_200_OK)


class PlaylistSaveAlbumView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, playlist_id, album_id):
        try:
            playlist = Playlist.objects.get(playlist_id=playlist_id, created_by=request.user)
        except Playlist.DoesNotExist:
            return Response({"detail": "Playlist not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            album = Album.objects.get(album_id=album_id)
        except Album.DoesNotExist:
            return Response({"detail": "Album not found."}, status=status.HTTP_404_NOT_FOUND)


        if album in playlist.albums.all():
            playlist.albums.remove(album)
            album_removed = True
        else:
            playlist.albums.add(album)
            album_removed = False


        added_count = 0
        removed_count = 0
        for song in album.song.all():
            if song in playlist.songs.all():
                playlist.songs.remove(song)
                removed_count += 1
            else:
                playlist.songs.add(song)
                added_count += 1

        if album_removed:
            message = f"Album '{album.album_name}' removed from playlist."
        else:
            message = f"Album '{album.album_name}' added to playlist."

        return Response({"detail": message}, status=status.HTTP_200_OK)
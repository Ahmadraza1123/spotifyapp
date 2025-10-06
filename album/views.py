from rest_framework import  status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Album
from .serializers import AlbumSerializer
from song.permissions import IsSingerOrReadOnly
from rest_framework.permissions import IsAuthenticated



class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated, IsSingerOrReadOnly]
    lookup_field = "album_id"

    def get_queryset(self):
        user = self.request.user
        if user.role == "singer":
            return Album.objects.filter(singer=user)
        return Album.objects.all()

    def perform_create(self, serializer):
        serializer.save(singer=self.request.user)

class AlbumLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, album_id):
        try:
            album = Album.objects.get(album_id=album_id)
        except Album.DoesNotExist:
            return Response({"detail": "Album not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if album.singer == user:
            return Response({"detail": "You cannot like your own album"}, status=status.HTTP_400_BAD_REQUEST)

        if user in album.Like.all():
            album.Like.remove(user)
            message = "Album like removed"
        else:
            album.Like.add(user)
            album.Unlike.remove(user)
            message = "Album liked"

        return Response({
            "detail": message,
            "like_count": album.Like.count(),
            "unlike_count": album.Unlike.count()
        }, status=status.HTTP_200_OK)


class AlbumDislikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, album_id):
        try:
            album = Album.objects.get(album_id=album_id)
        except Album.DoesNotExist:
            return Response({"detail": "Album not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if album.singer == user:
            return Response({"detail": "You cannot dislike your own album"}, status=status.HTTP_400_BAD_REQUEST)

        if user in album.Unlike.all():
            album.Unlike.remove(user)
            message = "Album dislike removed"
        else:
            album.Unlike.add(user)
            album.Like.remove(user)
            message = "Album disliked"

        return Response({
            "detail": message,
            "like_count": album.Like.count(),
            "unlike_count": album.Unlike.count()
        }, status=status.HTTP_200_OK)




class AlbumSaveLibraryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, album_id):
        try:
            album = Album.objects.get(album_id=album_id)
        except Album.DoesNotExist:
            return Response({"detail": "pl not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if user in album.saved_by.all():
            album.saved_by.remove(user)
            message = "album removed from your library"
        else:
            album.saved_by.add(user)
            message = "album saved to your library"

        album.save()
        return Response({"detail": message}, status=status.HTTP_200_OK)

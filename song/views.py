from rest_framework import generics,status,viewsets,filters
from rest_framework.permissions import IsAuthenticated
from .models import Song
from .serializers import SongSerializer
from .permissions import IsSingerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsSingerOrReadOnly]


    filter_backends = [filters.SearchFilter]
    search_fields = ['song_name','album_name__album_name','album_name__singer__username']

    def get_serializer_context(self):

        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)
class SongDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsSingerOrReadOnly]


class SongLikeDislikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, song_id, action):
        try:
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
            return Response({"detail": "Song not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if song.owner == user:
            return Response(
                {"detail": "Sorry, you cannot like/dislike your own song"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if action == "like":
            if user in song.Like.all():
                song.Like.remove(user)
                message = "Song like removed"
            else:
                song.Like.add(user)
                song.Unlike.remove(user)
                message = "Song liked"

        elif action == "dislike":
            if user in song.Unlike.all():
                song.Unlike.remove(user)
                message = "Song dislike removed"
            else:
                song.Unlike.add(user)
                song.Like.remove(user)
                message = "Song disliked"

        else:
            return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        song.save()
        return Response({"detail": message}, status=status.HTTP_200_OK)


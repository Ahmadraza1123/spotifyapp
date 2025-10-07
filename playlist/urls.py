from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaylistViewSet, PlaylistSaveSongView,PlaylistSaveAlbumView

router = DefaultRouter()
router.register(r'crud', PlaylistViewSet, basename='crud')

urlpatterns = [
    path('', include(router.urls)),

    path('<int:playlist_id>/song/<int:song_id>/save/', PlaylistSaveSongView.as_view(), name='playlist-save-song'),

    path('<int:playlist_id>/album/<int:album_id>/save/', PlaylistSaveAlbumView.as_view(), name='playlist-save-song'),

]

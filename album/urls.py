from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (AlbumViewSet,AlbumLikeView,AlbumDislikeView,AlbumSaveLibraryView,)

router = DefaultRouter()
router.register(r'crud', AlbumViewSet, basename='album')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:album_id>/like/', AlbumLikeView.as_view(), name='album-like'),
    path('<int:album_id>/dislike/', AlbumDislikeView.as_view(), name='album-dislike'),
    path('<int:album_id>/save/', AlbumSaveLibraryView.as_view(), name='album-save-playlist'),
]

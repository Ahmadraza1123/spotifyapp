from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SongViewSet, SongLikeDislikeView

router = DefaultRouter()
router.register(r'crud', SongViewSet, basename='crud')

urlpatterns = [
    path("", include(router.urls)),
    path("<int:song_id>/<str:action>/", SongLikeDislikeView.as_view(), name="song-like-dislike"),
]

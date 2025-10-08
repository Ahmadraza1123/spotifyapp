from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSingerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'singer'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True


        if hasattr(obj, 'singer'):
            return obj.singer == request.user

        if hasattr(obj, 'album_name') and obj.album_name:
            return obj.album_name.singer == request.user

        return hasattr(obj, 'owner') and obj.owner == request.user

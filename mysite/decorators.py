from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def required(view_func):

    @wraps(view_func)
    def wrapper(request):
        if not request.user.is_authenticated:
            return Response( status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_staff:
            return Response( status=status.HTTP_403_FORBIDDEN)
        return view_func(request)
    return wrapper

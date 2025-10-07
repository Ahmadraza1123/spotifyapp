from rest_framework import generics,status,permissions
from .models import CustomUser,PasswordReset
from .serializers import UserRegisterSerializer,LoginSerializer,UserProfileSerializer,ResetPasswordRequestSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
import os
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]



class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]


        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "token": token.key,
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:

            Token.objects.filter(user=request.user).delete()
            return Response(
                {"message": "Logout successful. Token deleted."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = CustomUser.objects.filter(email__iexact=email).first()

        if not user:
            return Response(
                {"error": "User with this email not found"},
                status=status.HTTP_404_NOT_FOUND
            )


        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)


        PasswordReset.objects.create(email=email, token=token)

        base_url = os.environ.get("PASSWORD_RESET_BASE_URL", "http://localhost:3000/reset-password")
        reset_url = f"{base_url}/{token}"

        send_mail(
            subject="Password Reset Request",
            message=f"Hi {user.username},\n\nUse the link below to reset your password:\n{reset_url}\n\nIf you did not request this, please ignore this email.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response(
            {"success": "We have sent you a link to reset your password"},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not all([email, token, new_password]):
            return Response(
                {"detail": "Email, token, and new_password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )


        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "Password has been reset successfully."},
            status=status.HTTP_200_OK
        )



class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)

        if target_user == request.user:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)


        if request.user.role != "normal" or target_user.role != "singer":
            return Response({"error": "Only normal users can follow singers"}, status=status.HTTP_403_FORBIDDEN)

        if target_user in request.user.following.all():
            return Response({"error": "Already following this user"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target_user)
        request.user.unfollowed.remove(target_user)

        return Response({
            "message": f"You are now following {target_user.username}",
            "following_count": request.user.following.count(),
            "followers_count": target_user.followers.count(),
        }, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)

        if target_user == request.user:
            return Response({"error": "You cannot unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.role != "normal" or target_user.role != "singer":
            return Response({"error": "Only normal users can unfollow singers"}, status=status.HTTP_403_FORBIDDEN)

        if target_user in request.user.following.all():
            return Response({"error": "Already unfollowing this user"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target_user)
        request.user.unfollowed.remove(target_user)

        return Response({
            "message": f"You are now unfollowing {target_user.username}",
            "following_count": request.user.following.count(),
            "followers_count": target_user.followers.count(),
        }, status=status.HTTP_200_OK)

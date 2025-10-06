from rest_framework import serializers
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from album.models import Album
from song.models import Song
User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)


    class Meta:
        model = CustomUser
        fields = ["id","username", "email","profile_image", "password", "password2", "role", "Bio"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser(
            username=validated_data["username"],
            email=validated_data["email"],
            role=validated_data["role"],
            profile_image=validated_data["profile_image"],
            Bio=validated_data["Bio"],
        )
        user.set_password(validated_data["password"])
        user.save()
        subject = "Welcome to Spotify App!"
        message = f"Hello {user.username},\n\nYour account has been created successfully.\nRole: {user.role}\n\nEnjoy!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password")

        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    total_albums = serializers.SerializerMethodField()
    total_songs = serializers.SerializerMethodField()
    album_song = serializers.SerializerMethodField()
    without_album_song = serializers.SerializerMethodField()
    Follow_count = serializers.SerializerMethodField()
    Unfollow_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'profile_image','total_albums', 'album_song','without_album_song', 'total_songs',"Follow_count","Unfollow_count",]

    def get_total_albums(self, obj):
        return Album.objects.filter(singer=obj).count()

    def get_album_song(self, obj):
        return Song.objects.filter(owner=obj).exclude(album_name__isnull=True).count()

    def get_without_album_song(self, obj):
        return Song.objects.filter(owner=obj, album_name__isnull=True).count()

    def get_total_songs(self, obj):
        return Song.objects.filter(owner=obj).count()

    def get_Follow_count(self, obj):
        return obj.followers.count()

    def get_Unfollow_count(self, obj):
        return obj.following.count()




class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        self.context["user"] = user
        return value

    def save(self):
        user = self.context["user"]
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        reset_token = f" Token {token}/"

        send_mail(
            subject="Password Reset Request",
            message=f"Hello {user.username},\n\nThis Token Put the Header to reset your password:\n{reset_token}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return {"detail": "Password reset link sent to email"}


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):

        from Account.models import CustomUser
        if not CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value
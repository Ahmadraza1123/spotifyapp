from django.urls import path
from .views import UserRegisterView,UserLoginView,UserProfileView,LogoutView,RequestPasswordReset,PasswordResetConfirmView,FollowUserView,UnfollowUserView

urlpatterns = [
    path("register/", UserRegisterView.as_view()),
    path("login/", UserLoginView.as_view()),
    path("profile/", UserProfileView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("password-reset/",RequestPasswordReset.as_view()),
    path("password-reset-confirm/",PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path("<int:user_id>/follow/", FollowUserView.as_view(), name="follow_user"),
    path("<int:user_id>/unfollow/", UnfollowUserView.as_view(), name="unfollow_user"),

]

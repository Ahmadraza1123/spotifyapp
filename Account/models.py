from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("singer", "Singer"),
        ("normal", "Normal"))

    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to="covers", blank=True)
    Bio = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    following = models.ManyToManyField("self",symmetrical=False,related_name="followers",blank=True)
    unfollowed = models.ManyToManyField("self",symmetrical=False,related_name="unfollowed_by",blank=True)



class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


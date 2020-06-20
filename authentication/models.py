from django.contrib.auth import authenticate
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from authentication.signals import create_profile
from main.models import UserProfile


class User(AbstractUser):
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    email_verification_date = models.DateTimeField(null=True)

    def get_profile(self):
        user_profile = UserProfile.objects.get(user=self)
        return user_profile

    # to be discussed with yehia
    def reset_password(self, token, token_created_at, token_is_used, token_deleted_at):
        """reset the users password by sending a token to his email"""
        pass


post_save.connect(create_profile, sender=User)

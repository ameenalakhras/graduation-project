from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from authentication.signals import create_profile
from main.models import UserProfile

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    email_verification_date = models.DateTimeField()

    def get_profile(self):
        user_profile = UserProfile.objects.get(user=self)
        return user_profile

    # to be discussed with yehia
    def reset_password(user_object, token, token_created_at, token_is_used, token_deleted_at):
        pass


post_save.connect(create_profile, sender=CustomUser)

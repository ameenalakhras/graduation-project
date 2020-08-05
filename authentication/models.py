from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from authentication.choices import TOKEN_TYPES
from authentication.signals import create_profile
from main.models import UserProfile, BaseModel
from rest_framework.authtoken.models import Token

import binascii
import os


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


class CustomToken(BaseModel):
    """
    The default token model for password rest / sign up email validation.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='custom_tokens',
        on_delete=models.CASCADE, verbose_name=_("User")
    )

    created = models.DateTimeField(_("Created"), auto_now_add=True)
    expired = models.BooleanField(default=False)
    # if the key was reported as a false attempt to rest password / sign up
    # this should be true
    destroyed = models.BooleanField(default=False)
    destruction_date = models.DateTimeField(null=True)
    _type = models.CharField(choices=TOKEN_TYPES, max_length=30)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


post_save.connect(create_profile, sender=User)

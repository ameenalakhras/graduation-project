from django.conf import settings
from django.db import models

from main.models import BaseModel
from django.utils.translation import gettext_lazy as _


class FCMToken(BaseModel):
    """
    token for firebase cloud messaging (used for android push notifications)
    """

    key = models.CharField(_("Key"), max_length=1000, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='fcm_token',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return (self.key)


class PushMessages(BaseModel):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='push_messages')
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=250)

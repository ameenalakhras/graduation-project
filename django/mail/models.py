from django.db import models
from django.conf import settings

from main.models import SoftDeleteModel

# Create your models here.

class Email(SoftDeleteModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="email_sender")
    receiver = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="receiver_users")
    title = models.CharField(max_length=50)
    context = models.TextField()
    received = models.BooleanField(default=False)
    received_at = models.DateTimeField()
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField()

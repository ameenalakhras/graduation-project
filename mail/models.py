from django.db import models
from django.conf.settings import AUTH_USER_MODEL

from main.models import SoftDeleteModel, BaseModel

# Create your models here.

class Email(SoftDeleteModel, BaseModel):
    sender = models.ForeignKey(AUTH_USER_MODEL)
    receiver = models.ManyToManyField(AUTH_USER_MODEL)
    title = models.CharField(max_length=50)
    context = models.TextField()
    received = models.BooleanField(default=False)
    received_at = models.DateTimeField()
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField()

from django.db import models
from main.models import SoftDeleteModel, BaseModel
from django.conf import settings
from classroom.models import ClassRoom
# Create your models here.

class Provider(SoftDeleteModel):
    """ the videos providor (youtube or another source)"""
    name = models.CharField(max_length=50)

class MediaType(SoftDeleteModel):
    """
    for example:
        in youtube provider:
            it can be 'playlist' or 'video'
    """
    name = models.CharField(max_length=50)


class Media(SoftDeleteModel):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name="media_classroom")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="media_publisher")
    _type = models.ForeignKey(MediaType, on_delete=models.CASCADE, related_name="media_type")
    #youtube as default
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="media_providor")
    path = models.URLField()

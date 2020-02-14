from django.db import models
from main.models import SoftDeleteModel, BaseModel
from django.conf.settings import AUTH_USER_MODEL

# Create your models here.

class Provider(SoftDeleteModel, BaseModel):
    """ the videos providor (youtube or another source)"""
    name = models.CharField(max_length=50)

class MediaType(SoftDeleteModel, BaseModel):
    """
    for example:
        in youtube provider:
            it can be 'playlist' or 'video'
    """
    name = models.CharField(max_length)


class Media(SoftDeleteModel, BaseModel):
    classroom = models.ForeignKey(AUTH_USER_MODEL)
    publisher = models.ForeignKey(AUTH_USER_MODEL)
    _type = models.ForeignKey(MediaType, on_delete=models.CASCADE)
    #youtube as default
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    path = models.UrlField()

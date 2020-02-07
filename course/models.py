from django.db import models

# Create your models here.

class Provider():
    """ the videos providor (youtube or another source)"""
    name = models.CharField(max_length=50)

class MediaType():
    """
    for example:
        in youtube provider:
            it can be 'playlist' or 'video'
    """
    name = models.CharField(max_length)


class Media():
    classroom = models.ForeignKey(AUTH_USER_MODEL)
    publisher = models.ForeignKey(AUTH_USER_MODEL)
    _type = models.ForeignKey(MediaType, on_delete=models.CASCADE)
    #youtube as default
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    path = models.UrlField()

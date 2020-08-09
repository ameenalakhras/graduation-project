from django.db import models
from django.db.models.signals import post_save, pre_save

from classroom.utils import default_avatar_img
from course.choices import PROVIDER_CHOICES
from course.utils import create_video_details
from main.models import BaseModel
from django.conf import settings
from classroom.models import ClassRoom
from main.utils import get_avatar_path, get_thumbnail_path


class Course(BaseModel):
    classroom = models.ManyToManyField(ClassRoom, related_name="classroom_courses")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="media_publisher")
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)


class Media(BaseModel):
    title = models.CharField(max_length=300, null=True)
    description = models.TextField(max_length=5000, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="media")
    provider = models.CharField(choices=PROVIDER_CHOICES, default=PROVIDER_CHOICES[0][0], max_length=30)
    path = models.URLField()
    thumbnail = models.ImageField(
        upload_to=get_thumbnail_path, default=default_avatar_img(),
        max_length=1000, null=True
    )


pre_save.connect(create_video_details, sender=Media)

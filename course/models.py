from django.db import models

from classroom.utils import default_avatar_img
from course.choices import PROVIDER_CHOICES
from main.models import BaseModel
from django.conf import settings
from classroom.models import ClassRoom
from main.utils import get_avatar_path


class Course(BaseModel):
    classroom = models.ManyToManyField(ClassRoom, related_name="classroom_courses")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="media_publisher")
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)


class Media(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course")
    provider = models.CharField(choices=PROVIDER_CHOICES, default=PROVIDER_CHOICES[0][0], max_length=30)
    path = models.URLField()
    thumbnail = models.ImageField(
        upload_to=get_avatar_path, default=default_avatar_img(),
        max_length=1000, null=True
    )

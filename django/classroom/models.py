from django.db import models
from django.conf import settings

from classroom.utils import get_classroom_logo_image, get_classroom_bg_image

from main.models import SoftDeleteModel, BaseModel, Attachment
from main.utils import get_storage
# AUTH_USER_MODEL =

class ClassRoom(SoftDeleteModel):
    title = models.CharField(max_length=50)
    logo_img = models.ImageField(upload_to=get_classroom_logo_image, storage=get_storage())
    background_img = models.ImageField(upload_to=get_classroom_bg_image, storage=get_storage())

    description = models.TextField
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attachments = models.ManyToManyField(Attachment)


class ClassRoomTeacher(SoftDeleteModel):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Post(SoftDeleteModel):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()


class Comments(SoftDeleteModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #defaulted as 0 if it was a comment on a post, if it was a reply on a comment it will take the comment id
    parent_id = models.IntegerField(default=0)
    content = models.TextField()


class Task(SoftDeleteModel):
    degree = models.IntegerField()
    # creator: originally a teacher or an assistant
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    # attachments = models.ManyToManyField(Attachment)

class TaskSOlutionInfo(SoftDeleteModel):
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    notes = models.CharField(max_length=300)
    accepted = models.BooleanField(default=False)

class TaskSolution(SoftDeleteModel):
    accepted = models.BooleanField(default=False)
    solutionInfo = models.ManyToManyField(Attachment)
    task = models.OneToOneField(Task, on_delete=models.CASCADE)



# # many to many relation
# class ClassroomAttchment(SoftDeleteModel):
#     attachment (FK to attachment)
#     classroom (FK to classroom)

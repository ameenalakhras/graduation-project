from django.db import models
from django.conf import settings

from classroom.utils import get_classroom_bg_path, get_classroom_logo_path

from main.models import SoftDeleteModel, BaseModel, Attachment
from main.utils import get_storage

from classroom.utils import default_class_logo_img, default_class_background_img


class ClassRoom(SoftDeleteModel):
    title = models.CharField(max_length=50)
    logo_img = models.ImageField(
                                upload_to=get_classroom_logo_path,
                                storage=get_storage(), null=True,
                                default=default_class_logo_img(),
                                max_length=1000
    )
    background_img = models.ImageField(
                                    upload_to=get_classroom_bg_path, storage=get_storage(),
                                    null=True, default=default_class_background_img(),
                                    max_length=1000
    )
    description = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher_classrooms")
    attachments = models.ManyToManyField(Attachment, blank=True)
    promo_code = models.CharField(max_length=20, unique=True)
    allow_student_participation = models.BooleanField(default=True)
    auto_accept_students = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="student_classrooms", blank=True)
    student_requests = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="classroom_request", blank=True)


class Post(SoftDeleteModel):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name="class_posts")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_posts")
    content = models.TextField()


class Comments(SoftDeleteModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
    # defaulted as 0 if it was a comment on a post, if it was a reply on a comment it will take the comment id
    parent_id = models.IntegerField(default=0)
    content = models.TextField()


class Material(SoftDeleteModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_material")
    classroom = models.ManyToManyField(ClassRoom, related_name="classroom_material", blank=True)
    file = models.FileField(max_length=1000)


class Task(SoftDeleteModel):
    average_degree = models.IntegerField(null=True)
    # creator: originally a teacher or an assistant
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    attachments = models.ManyToManyField(Attachment, blank=True)


class TaskSolutionInfo(SoftDeleteModel):
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    notes = models.CharField(max_length=300, null=True)
    accepted = models.BooleanField(null=True)


class TaskSolution(SoftDeleteModel):
    accepted = models.BooleanField(null=True)
    solutionInfo = models.ManyToManyField(Attachment, blank=True)
    task = models.OneToOneField(Task, on_delete=models.CASCADE)

from django.db import models
from main.utils import get_avatar_path
from django.conf import settings


class BaseModel(models.Model):
    """
    a Base Model to load the create_date and modified_date
    fields into all the tables in the DataBase
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(BaseModel):
    deleted_at = models.DateTimeField()
    deleted = models.BooleanField(default=False)

    def delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        super.save()

    # telling django that the SoftDeleteModel is an abstract class
    class Meta:
        abstract = True



class UserProfile(SoftDeleteModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=get_avatar_path)

    def __str__(self):
        return self.user.username


class Notification(BaseModel):
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    content = models.CharField(max_length=1000)

    read_at = models.DateTimeField()
    received_at = models.DateTimeField()


class AttachmentType(BaseModel):
    """
        'classroom' or 'task attachment' for now
    """
    name = models.CharField(max_length=50)


class Attachment(SoftDeleteModel):
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    file = models.FileField()
    _type = models.ForeignKey(AttachmentType, on_delete=models.CASCADE)



#
# class Permissions():
#     permission_id
#     permission_name
#
# class Role():
#     role_id
#     role_name
#
#
# class Taggable_permission():
#     taggable_type
#     permission( 'FK from Permission class' )
#     taggable_id('just an integer (to point to ClassRoomTeacher or Role [depending on taggable_type])')
#
# """
# example:
# if taggable_permission_object.taggable_type == "class_room_teacher":
#     if taggable_permission_object.permission.permission_name == "classroom_creator":
#         give him access
#     elif permission == "teacher assistant":
#         don't give him access
# """


#
# class SettingsKeys():
#     name = models.CharField(max_length = 50)
#
# class SettingsKeysValues():
#     key = models.ForeignKey(SettingsKeys, on_delete=models.CASCADE)
#     value = models.CharField(max_length = 50)
#
# class SettingsValues(BaseModel):
#     """this holds the settings values that the app uses
#     (the option itself can be picked by a drop down its values coming
#     from SettingsOptions Model)"""
#     key
#     value (FK from 'SettingsOptions' [filtered by the key = value ])

# class SettingsOptions():
#     """this holds the different values(options) for different keys"""
#     key = models.OneToOneField(SSettingsKeys)
#     value

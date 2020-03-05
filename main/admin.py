from django.contrib import admin

from main.models import BaseModel, SoftDeleteModel, UserProfile, Notification, AttachmentType, Attachment
# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Notification)
admin.site.register(AttachmentType)
admin.site.register(Attachment)

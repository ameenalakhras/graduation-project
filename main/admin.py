from django.contrib import admin

from main.models import UserProfile, Notification, Attachment
# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Notification)
admin.site.register(Attachment)

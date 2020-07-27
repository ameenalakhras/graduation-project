from django.contrib import admin

from authentication.models import User, CustomToken, FCMToken, PushMessages
# Register your models here.

admin.site.register(User)
admin.site.register(CustomToken)
admin.site.register(FCMToken)
admin.site.register(PushMessages)

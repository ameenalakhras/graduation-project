from django.contrib import admin

from fcm_service.models import FCMToken, PushMessages

admin.site.register(FCMToken)
admin.site.register(PushMessages)

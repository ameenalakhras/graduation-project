from django.contrib import admin

from authentication.models import User, CustomToken

admin.site.register(User)
admin.site.register(CustomToken)

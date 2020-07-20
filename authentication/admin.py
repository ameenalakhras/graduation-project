from django.contrib import admin

from authentication.models import User, CustomToken
# Register your models here.

admin.site.register(User)
admin.site.register(CustomToken)

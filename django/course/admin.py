from django.contrib import admin

from course.models import Media, MediaType, Provider
# Register your models here.

admin.site.register(Media)
admin.site.register(MediaType)
admin.site.register(Provider)

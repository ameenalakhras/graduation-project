from rest_framework import serializers

from course.models import Media
from main.serializers import soft_delete_fields


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = soft_delete_fields

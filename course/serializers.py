from rest_framework import serializers

from course.models import Media, Course
from main.serializers import soft_delete_fields
from authentication.serializers import UserSerializer


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = soft_delete_fields


class CourseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user = UserSerializer()

    class Meta:
        model = Course
        exclude = soft_delete_fields

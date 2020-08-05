from rest_framework import serializers

from course.models import Media, Course
from authentication.serializers import UserSerializer


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title", "description")


class CourseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_info = UserSerializer(source="user", read_only=True)
    media = MediaSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = "__all__"

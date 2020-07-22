from rest_framework import serializers

from course.models import Media, Course
from authentication.serializers import UserSerializer


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_info = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

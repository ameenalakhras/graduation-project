from rest_framework import serializers

from classroom.models import ClassRoom, Comments, Task, Post, ClassRoomTeacher
from main.serializers import soft_delete_fields



class ClassRoomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = ClassRoom
        exclude = soft_delete_fields


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = Comments
        exclude = soft_delete_fields


# the task serializer should make sure it's a teacher who is making the task
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = soft_delete_fields


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = soft_delete_fields


class ClassRoomTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoomTeacher
        exclude = soft_delete_fields

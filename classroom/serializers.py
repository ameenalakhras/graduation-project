from rest_framework import serializers

from classroom.models import ClassRoom, Comments, Task, Post#, ClassRoomTeacher
from main.serializers import soft_delete_fields

from authentication.serializers import UserSerializer


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    commenter = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Comments
        exclude = soft_delete_fields


class PostSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(source="post_comments", many=True, read_only=True)

    class Meta:
        model = Post
        exclude = soft_delete_fields


class ClassRoomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    student_objects = UserSerializer(source="students", many=True, read_only=True)
    student_requests_objects = UserSerializer(source="student_requests", many=True, read_only=True)
    posts = PostSerializer(source="class_posts", many=True, read_only=True)


    class Meta:
        model = ClassRoom
        exclude = soft_delete_fields + ("students", "student_requests")



# the task serializer should make sure it's a teacher who is making the task
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = soft_delete_fields




# class ClassRoomTeacherSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClassRoomTeacher
#         exclude = soft_delete_fields

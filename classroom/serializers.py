from rest_framework import serializers

from classroom.models import ClassRoom, Comments, Task, Post, Material#, ClassRoomTeacher
from main.serializers import soft_delete_fields

from authentication.serializers import UserSerializer


class MaterialSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    uploader = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Material
        exclude = soft_delete_fields + ("classroom", "id")


class ClassroomMaterialSerializer(MaterialSerializer):
    """
    the same material serializer but this one is for create requests, it doesn't exclude the classroom
    since it is saved in the database in the create request.
    """
    class Meta:
        model = Material
        exclude = soft_delete_fields + ("id", )


class PutMaterialSerializer(MaterialSerializer):
    """
    the same material serializer but this one is for edit requests (put), it excludes the user
    since changing him will change the authority for the material owner himself.
    """
    class Meta:
        model = Material
        fields = ("file", )


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
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

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
    material = MaterialSerializer(source="classroom_material", many=True, read_only=True)

    class Meta:
        model = ClassRoom
        exclude = soft_delete_fields + ("students", "student_requests")


# the task serializer should make sure it's a teacher who is making the task
class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Task
        exclude = soft_delete_fields


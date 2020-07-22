from rest_framework import serializers

from classroom.models import ClassRoom, Comments, Task, Post, Material, TaskSolutionInfo, \
    TaskSolution  # , ClassRoomTeacher
from main.serializers import soft_delete_fields, AttachmentSerializer

from authentication.serializers import UserSerializer


class MaterialSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_info = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Material
        exclude = soft_delete_fields + ("classroom",)


class ClassroomMaterialSerializer(MaterialSerializer):
    """
    the same material serializer but this one is for create requests, it doesn't exclude the classroom
    since it is saved in the database in the create request.
    """
    class Meta:
        model = Material
        exclude = soft_delete_fields + ("id", )


class EditMaterialSerializer(MaterialSerializer):
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
    user_info = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Comments
        exclude = soft_delete_fields


class CommentsUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('content', )


class PostSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(source="post_comments", many=True, read_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_info = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Post
        exclude = soft_delete_fields


class PostUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("content", )


# the task serializer should make sure it's a teacher who is making the task




class EditClassRoomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = ClassRoom
        exclude = soft_delete_fields + ("students", "student_requests", "promo_code", "archived", )


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "content", "attachments", "accept_solutions", "accept_solutions_due")


class TaskSolutionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSolutionInfo
        fields = ("notes", "id")


class TaskSolutionInfoUpdateSerializer(serializers.ModelSerializer):
    """
    this class serves as the update serializer for the teacher to submit  the task solution status
     (accepted or not).
    """
    class Meta:
        model = TaskSolutionInfo
        fields = ("accepted", )


class TaskSolutionSerializer(serializers.ModelSerializer):
    solutionInfo = TaskSolutionInfoSerializer()

    class Meta:
        model = TaskSolution
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_info = UserSerializer(source="user", read_only=True)
    attachments_info = AttachmentSerializer(source="attachments", read_only=True, many=True)
    solutions = TaskSolutionInfoSerializer(source="students")

    class Meta:
        model = Task
        exclude = soft_delete_fields


class ClassRoomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_info = UserSerializer(source="user", read_only=True)
    student_objects = UserSerializer(source="students", many=True, read_only=True)
    student_requests_objects = UserSerializer(source="student_requests", many=True, read_only=True)
    posts = PostSerializer(source="class_posts", many=True, read_only=True)
    material = MaterialSerializer(source="classroom_material", many=True, read_only=True)
    classroom_tasks_info = TaskSerializer(source="classroom_tasks", many=True, read_only=True)

    class Meta:
        model = ClassRoom
        exclude = soft_delete_fields + ("students", "student_requests")

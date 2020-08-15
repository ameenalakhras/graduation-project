from rest_framework import serializers

from classroom.models import ClassRoom, Comments, Task, Post, Material, TaskSolutionInfo, \
    TaskSolution  # , ClassRoomTeacher
from course.serializers import CourseSerializer
from main.serializers import AttachmentSerializer

from authentication.serializers import UserSerializer


class MaterialSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_info = UserSerializer(source="user", read_only=True)
    attachment_info = AttachmentSerializer(source="attachment", read_only=True)

    class Meta:
        model = Material
        exclude = ("classroom", "file")


class ClassroomMaterialSerializer(MaterialSerializer):
    """
    the same material serializer but this one is for create requests, it doesn't exclude the classroom
    since it is saved in the database in the create request.
    """
    class Meta:
        model = Material
        exclude = ("file", )


class EditMaterialSerializer(MaterialSerializer):
    """
    the same material serializer but this one is for edit requests (put), it excludes the user
    since changing him will change the authority for the material owner himself.
    """
    class Meta:
        model = Material
        fields = ('id', "attachment")


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_info = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Comments
        fields = "__all__"


class CommentsUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('id', 'content')


class PostSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(source="post_comments", many=True, read_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_info = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_info = UserSerializer(source="user", read_only=True)
    comments_count = serializers.IntegerField(
        source='post_comments.count',
        read_only=True
    )

    class Meta:
        model = Post
        exclude = ("classroom", )


class PostUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "content")


class EditClassRoomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = ClassRoom
        exclude = ("id", "students", "student_requests", "promo_code", "archived", )


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "content", "attachments", "accept_solutions", "accept_solutions_due")


class TaskSolutionInfoSerializer(serializers.ModelSerializer):
    attachment_info = AttachmentSerializer(source="attachment", read_only=True)

    class Meta:
        model = TaskSolutionInfo
        fields = ("notes", "id", "attachment", "attachment_info")


class TaskSolutionInfoUpdateSerializer(serializers.ModelSerializer):
    """
    this class serves as the update serializer for the teacher to submit  the task solution status
     (accepted or not).
    """
    class Meta:
        model = TaskSolutionInfo
        fields = ("accepted", )


class TaskSolutionSerializer(serializers.ModelSerializer):
    solutionInfo = TaskSolutionInfoSerializer(many=True)

    class Meta:
        model = TaskSolution
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_info = UserSerializer(source="user", read_only=True)
    attachments_info = AttachmentSerializer(source="attachments", read_only=True, many=True)
    # solutions = TaskSolutionInfoSerializer(source="students", read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


class CleanClassRoomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_info = UserSerializer(source="user", read_only=True)
    students_count = serializers.IntegerField(
        source='students.count',
        read_only=True
    )
    students_requests_count = serializers.IntegerField(
        source='student_requests.count',
        read_only=True
    )
    material_count = serializers.IntegerField(
        source='classroom_material.count',
        read_only=True
    )
    tasks_count = serializers.IntegerField(
        source='classroom_tasks.count',
        read_only=True
    )
    course_count = serializers.IntegerField(
        source='classroom_courses.count',
        read_only=True
    )

    class Meta:
        model = ClassRoom
        exclude = ("student_requests", "attachments", "students")


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
    course = CourseSerializer(source="classroom_courses", many=True, read_only=True)

    class Meta:
        model = ClassRoom
        exclude = ("students", "student_requests")


class ListSubmittedTasksSolutionSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source="task.title")
    classroom_name = serializers.CharField(source="task.classroom.title")

    class Meta:
        model = TaskSolution
        fields = ("id", "task_title", "classroom_name", "task", "accepted")

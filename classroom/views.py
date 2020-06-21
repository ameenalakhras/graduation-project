from classroom.serializers import ClassRoomSerializer, CommentsSerializer, TaskSerializer,\
                                  PostSerializer#, ClassRoomTeacherSerializer
from classroom.models import ClassRoom, Comments, Task, Post#, ClassRoomTeacher
from composeexample.permissions import OwnerEditOnly

from django.contrib.auth.models import Group

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.filter(deleted=False)
    serializer_class = ClassRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        teachers_group = Group.objects.get(name="teachers")
        students_group = Group.objects.get(name="students")
        user = self.request.user
        user_group = self.request.user.groups.first()

        if user_group == students_group:
            return user.student_classrooms.filter(archived=False, deleted=False)
        elif user_group == teachers_group:
            return user.teacher_classrooms.filter(archived=False, deleted=False)
        else:
            return {"message": "user isn't registered in any group."}


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.filter(deleted=False)
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(deleted=False)
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(deleted=False)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly]

#
# class ClassRoomTeacherViewSet(viewsets.ModelViewSet):
#     queryset = ClassRoomTeacher.objects.filter(deleted=False)
#     serializer_class = ClassRoomTeacherSerializer
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['get','head', 'patch']

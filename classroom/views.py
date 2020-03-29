from classroom.serializers import ClassRoomSerializer, CommentsSerializer, TaskSerializer,\
                                  PostSerializer, ClassRoomTeacherSerializer
from classroom.models import ClassRoom, Comments, Task, Post, ClassRoomTeacher
from composeexample.permissions import OwnerEditOnly

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.filter(deleted=False)
    serializer_class = ClassRoomSerializer
    # permission_classes = [IsAuthenticated, OwnerEditOnly]


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


class ClassRoomTeacherViewSet(viewsets.ModelViewSet):
    queryset = ClassRoomTeacher.objects.filter(deleted=False)
    serializer_class = ClassRoomTeacherSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','head', 'patch']

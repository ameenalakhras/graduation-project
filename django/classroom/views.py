from classroom.serializers import ClassRoomSerializer, CommentsSerializer, TaskSerializer, PostSerializer, ClassRoomTeacherSerializer
from classroom.models import ClassRoom, Comments, Task, Post, ClassRoomTeacher

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# Create your views here.

class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class ClassRoomTeacherViewSet(viewsets.ModelViewSet):
    queryset = ClassRoomTeacher.objects.all()
    serializer_class = ClassRoomTeacherSerializer
    permission_classes = [IsAuthenticated]

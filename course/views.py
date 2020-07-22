from course.serializers import MediaSerializer, CourseSerializer
from course.models import Media, Course
from composeexample.permissions import OwnerEditOnly

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.filter(deleted=False)
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(deleted=False)
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly]

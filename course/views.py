from course.serializers import MediaSerializer, CourseSerializer, CourseListSerializer
from course.models import Media, Course
from composeexample.permissions import OwnerEditOnly

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all().order_by("-created_at")
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by("-created_at")
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly]

    def list(self, request, *args, **kwargs):
        self.serializer_class = CourseListSerializer
        super(CourseViewSet, self).list(request, *args, **kwargs)

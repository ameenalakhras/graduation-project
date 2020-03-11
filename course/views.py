from course.serializers import MediaSerializer
from course.models import Media

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.filter(deleted=False)
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]

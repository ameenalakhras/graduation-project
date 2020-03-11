from main.models import UserProfile, Attachment
from main.serializers import UserProfileSerializer, AttachmentSerializer#, NotificationSerializer
from composeexample.permissions import OwnProfilePermission

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

import datetime

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.filter(deleted=False)
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    # prevented "post" requests (making profile isn't allowed since it's auto generated)
    http_method_names = ['get', 'put', 'head', 'patch']


# class PermissionViewSet(viewsets.ModelViewSet):
#     queryset = Permission.objects.all()
#     serializer_class = PermissionSerializer
#     permission_classes = [IsAuthenticated]


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.filter(deleted=False)
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated, OwnProfilePermission]
    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)
#
# class SettingsOptionsSet(viewsets.ModelViewSet):
#     queryset = SettingsOptions.objects.all()
#     serializer_class = SettingsOptionsSerializer
#     permission_classes = [IsAuthenticated]
#
#
# class SettingsValuesSet(viewsets.ModelViewSet):
#     queryset = SettingsValues.objects.all()
#     serializer_class = SettingsValuesSerializer
#     permission_classes = [IsAuthenticated]

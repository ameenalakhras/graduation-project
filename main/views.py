from main.models import UserProfile, Attachment
from main.serializers import UserProfileSerializer, AttachmentSerializer, \
    AttachmentUpdateSerializer  # , NotificationSerializer
from composeexample.permissions import OwnerEditOnly

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

import datetime

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.filter()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly]
    # prevented "post" requests (making profile isn't allowed since it's auto generated)
    http_method_names = ['get', 'put', 'head', 'patch']


# class PermissionViewSet(viewsets.ModelViewSet):
#     queryset = Permission.objects.all()
#     serializer_class = PermissionSerializer
#     permission_classes = [IsAuthenticated]


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.filter()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated, OwnerEditOnly]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PATCH':
            serializer_class = AttachmentUpdateSerializer

        return serializer_class

    def list(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().filter(user=request.user)
        return super(AttachmentViewSet, self).list(request, *args, **kwargs)
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

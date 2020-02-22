from reservation.models import Room, Reserve
from api.serializers import RoomAvailableSerializer, ReserveSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

import datetime

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]



class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

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

from mail.serializers import MailSerializer
from mail.models import Mail

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class MailViewSet(viewsets.ModelViewSet):
    queryset = Mail.objects.all().order_by("-created_at")
    serializer_class = MailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
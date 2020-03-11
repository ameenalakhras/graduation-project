from mail.serializers import MailSerializer
from mail.models import Mail

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class MailViewSet(viewsets.ModelViewSet):
    queryset = Mail.objects.filter(deleted=False)
    serializer_class = MailSerializer
    permission_classes = [IsAuthenticated]

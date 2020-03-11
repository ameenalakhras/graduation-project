from rest_framework import serializers

from mail.models import Mail
from main.serializers import soft_delete_fields


class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        exclude = soft_delete_fields

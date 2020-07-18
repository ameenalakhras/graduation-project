from django.db import models
from django.conf import settings

from mail.email_purpose import EMAIL_TYPE_CHOICES
from main.models import SoftDeleteModel


class Mail(SoftDeleteModel):
    sender_email = models.EmailField()
    receiver_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="receiver_users")
    receivers_emails_txt = models.CharField(max_length=500)
    subject = models.CharField(max_length=50)
    html_content = models.TextField()
    sent = models.BooleanField(default=False)
    status_code = models.IntegerField()
    response_body = models.CharField(max_length=500)
    _type = models.IntegerField(choices=EMAIL_TYPE_CHOICES)

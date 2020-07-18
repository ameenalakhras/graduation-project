from django.conf import settings

from mail.models import Mail as MailModel

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_mail(to_users, subject, html_content, from_email=settings.DEFAULT_FROM_EMAIL, _type=1):
    # it it's a single user (not a list)
    if type(to_users) is not list:
        to_users = [to_users]

    to_emails = [user.email for user in to_users]

    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content,
    )

    sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = sendgrid_client.send(message)
    if response.status_code == 202:
        sent = True
    else:
        sent = False
    mail_obj = MailModel.objects.create(
        sender_email=from_email,
        receivers_emails_txt=str(to_emails),
        subject=subject,
        html_content=html_content,
        sent=sent,
        status_code=response.status_code,
        response_body=response.body,
        _type=1
    )
    mail_obj.receiver_users.set(to_users)
    mail_obj.save()
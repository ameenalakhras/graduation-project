from pyfcm import FCMNotification

from django.conf import settings
from django.shortcuts import get_object_or_404

from fcm_service.models import PushMessages, FCMToken

push_service = FCMNotification(api_key=settings.FCM_API_KEY)


def send_single_notifications(user, message_title, message_body):

    fcm_obj = get_object_or_404(FCMToken, user=user)

    result = push_service.notify_single_device(
        registration_id=fcm_obj.key,
        message_title=message_title,
        message_body=message_body
    )
    if result.get("success"):
        push_messages_obj = PushMessages.objects.create(
            title=message_title,
            body=message_body
        )

        push_messages_obj.users.add(user)
        push_messages_obj.save()

    return result


def send_multi_notifications(users, message_title, message_body):
    # Send to multiple devices by passing a list of ids.
    fcm_tokens_queryset = FCMToken.objects.filter(user__in=users)
    registration_ids = [token.key for token in fcm_tokens_queryset]
    result = push_service.notify_multiple_devices(
        registration_ids=registration_ids,
        message_title=message_title,
        message_body=message_body
    )
    if result.get("success"):
        push_messages_obj = PushMessages.objects.create(
            title=message_title,
            body=message_body
        )
        push_messages_obj.users.set(users)
        push_messages_obj.save()
    return result


def generate_title_and_body(request_type, data):
    if request_type == "post":
        title = f"new post in classroom {data.get('classroom').title}"
        description = f"{data.get('post_description')[:30]}"

    elif request_type == "task":
        title = f"new task in classroom {data.get('classroom').title}"
        description = f"task {data.get('task').title}"

    return title, description


def send_notification(user, request_type, data, many=True):
    title, description = generate_title_and_body(request_type, data)
    if many:
        result = send_multi_notifications(user, title, description)
    else:
        result = send_single_notifications(user, title, description)

    return result

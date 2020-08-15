from pyfcm import FCMNotification

from django.conf import settings
from django.shortcuts import get_object_or_404

from fcm_service.models import PushMessages, FCMToken

push_service = FCMNotification(api_key=settings.FCM_API_KEY)


def send_single_notifications(user, message_title, message_body):
    token_exists = FCMToken.objects.filter(user=user).exists()
    if not token_exists:
        return None
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
    if not fcm_tokens_queryset.exists():
        return None
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
        # data needed: classroom, post
        classroom = data.get('classroom')
        post = data.get('post')
        title = f"new post in classroom {classroom.title}"
        description = f"{post.content}"

    elif request_type == "task":
        # data needed: classroom, task
        task = data.get('task')
        classroom = data.get('classroom')
        title = f"new task in classroom {classroom.title}"
        description = f"task {task.title}"

    if request_type == "comment":
        # data needed: classroom, task
        comment = data.get('comment')
        title = f"{comment.user.first_name} has commented on your post"
        description = comment.content

    if request_type == "accept_or_reject_task_solution":
        solution = data.get("solution")
        solution_main_model = data.get('solution_main_model')
        if solution.accepted:
            status = 'accepted'
        else:
            status = "rejected"
        title = f"solution {status}"
        description = f"your solution to task {solution_main_model.task.title} has been {status}"

    return title, description


def send_notification(user, request_type, data, many=True):
    title, description = generate_title_and_body(request_type, data)
    if many:
        result = send_multi_notifications(user, title, description)
    else:
        result = send_single_notifications(user, title, description)

    return result

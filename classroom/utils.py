from django.conf import settings

from main.utils import generate_string_random_id, get_full_user_path


def get_classroom_logo_path(instance, filename):
    """return the avatar classroom logo image path"""
    random_id = generate_string_random_id()
    user_path = get_full_user_path(instance)
    return f'{user_path}/classroom/logos/{random_id}/{filename}'


def get_classroom_bg_path(instance, filename):
    """return the avatar classroom logo image path"""
    random_id = generate_string_random_id()
    user_path = get_full_user_path(instance)
    return f'{user_path}/classroom/backgrounds/{random_id}/{filename}'

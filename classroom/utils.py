from main.utils import generate_string_random_id, get_full_user_path
import uuid


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


def default_class_logo_img():
    return 'images/users/3/classroom/logos/eae50b1d-8ffc-41f8-b65d-aa51ebfd14d6/informationSec.jpg'


def default_class_background_img():
    return 'images/users/3/classroom/backgrounds/676c76b5-f361-46ce-a926-c3366855100f/header_classroom_default.png'


def default_avatar_img():
    return "images/users/2/avatar/ae015c75-a8d3-4253-8208-698b9dcf9323/default_medium_avatar.png"


def generate_promo_code(length=7):
    promo_code = str(uuid.uuid4())
    return promo_code[:7]

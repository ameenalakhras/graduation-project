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


def default_class_logo_img():
    return 'https://image.shutterstock.com/image-vector/shield-letter-s-logosafesecureprotection-logomodern-260nw-633031571.jpg'


def default_class_background_img():
    return 'https://3.bp.blogspot.com/-3OZFSKvugss/VzH53PuahJI/AAAAAAAABdc/rGczv9JzFFUH1wBMx7gTtJBNl44GjaeQwCLcB/s1600/desain%2Bbackground%2Bpermainan%2Bwarna%2B6.jpg'
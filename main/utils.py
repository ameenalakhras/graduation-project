from django.conf import settings
# random id generator
import uuid
# import ipdb; ipdb.set_trace()

def get_storage():
    return ''

def generate_string_random_id():
    """generate a ranodm string id then convert it to string"""
    random_id = uuid.uuid4()
    return str(random_id)

def get_full_user_path(instance):
    """return the full user path including the user id"""
    return f"{settings.DEFAULT_USER_PATH}/{instance.user.id}"

def get_avatar_path(instance, filename):
    """upload the avatar image and put the user name in the bath of the image """
    random_id = generate_string_random_id()
    user_path = get_full_user_path(instance)
    return f'{user_path}/avatar/{random_id}/{filename}'

def get_attchment_path(instance, filename):
    """return the attachemnt path that it should be in"""
    random_id = generate_string_random_id()
    user_path = get_full_user_path(instance)
    return f'{user_path}/attachments/{random_id}/{filename}'



def get_storage():
    return ''



def get_avatar_path(instance, filename):
    """upload the avatar image and put the user name in the bath of the image """
    return 'images/users/%s/avatar/%s' % (instance.user.id, filename)

from main.models import UserProfile


def create_profile(sender, instance, **kwargs):
    """signal handler to create a user profile after the account is created."""
    if kwargs["created"]:
        UserProfile.objects.create(user=instance)

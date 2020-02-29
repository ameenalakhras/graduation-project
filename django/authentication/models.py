from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from authentication.signals import create_profile
from main.models import UserProfile

class User(AbstractUser):
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    email_verification_date = models.DateTimeField(null=True)

    def get_profile(self):
        user_profile = UserProfile.objects.get(user=self)
        return user_profile

    # to be discussed with yehia
    def reset_password(user_object, token, token_created_at, token_is_used, token_deleted_at):
        """reset the users password by sending a token to his email"""
        pass

    def change_password(self, old_password, new_password):
        """change the old password by entering the previous password and the
        the new password"""
        user = authenticate(username=request.user.username, password=old_password)
        if user:
            if user == self.user:
                self.user.set_password(new_password)
                self.user.save()
                status = True
                message = "the password got changed"
            else:
                status = False
                # the system should log out the user at this time
                message = f"a security breach is detected from user '{self.user}' to user '{user}'"
        else:
            status = False
            message = "invalid credentials"
        return (status, message)



post_save.connect(create_profile, sender=User)

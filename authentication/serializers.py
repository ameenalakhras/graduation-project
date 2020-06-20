
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _
from django.core import exceptions

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from authentication.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "date_joined", "first_name", "last_name", "groups")

    def validate(self, attrs):
        try:
            validate_password(attrs['password'])
        except exceptions.ValidationError as e:
            raise exceptions.ValidationError(e)
        else:
            attrs['password'] = make_password(attrs['password'])
            return attrs


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        try:
            self.user = User.objects.get(username=attrs.get("username"))
        except User.DoesNotExist:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])
        else:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])

            self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
            if self.user:
                return attrs
            else:
                raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class UserPasswordChangeSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    default_error_messages = {
        'invalid_old_password': _('Old password is invalid'),
        'invalid_new_password': _('You need a stronger Password'),
    }

    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):

        # make sure the password is strong enough through django validation
        try:
            password_validation.validate_password(attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(self.error_messages['invalid_new_password'])

        self.user = attrs.get("user")
        valid_password = self.user.check_password(raw_password=attrs.get("old_password"))
        if valid_password:
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_old_password'])


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token", "created")
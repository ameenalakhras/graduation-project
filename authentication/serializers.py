
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from authentication.errors import CustomValidationError
from authentication.models import User, CustomToken, FCMToken, PushMessages
from main.serializers import UserProfileSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "groups", "profile"]


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


class CustomTokenSerializer(serializers.ModelSerializer):
    key = serializers.ReadOnlyField()

    class Meta:
        model = CustomToken
        fields = ("key", "user", "_type")


class CustomTokenRetrieveDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomToken
        fields = ("key", )


# serializers.Serializer doesn't take Meta which makes it perfect for such cases (without models)
class ResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(required=True)

    default_error_messages = {
        'invalid_password': _('You need a stronger Password'),
    }

    def validate(self, attrs):
        # make sure the password is strong enough through django validation
        try:
            password_validation.validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(self.error_messages['invalid_password'])
        else:
            return attrs


class FCMTokenSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    def is_valid(self, *args, **kwargs):
        try:
            data = self.run_validation(self.initial_data)
        except ValidationError as e:
            # if it's the error that the key is unique
            if e.get_codes()["key"][0] == "unique":
                raise CustomValidationError("key already exists (duplicated key)", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                raise e
        else:

            try:
                fcm_token_exists = data.get("user").fcm_token
                raise CustomValidationError("user already has a key.", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

            except User.fcm_token.RelatedObjectDoesNotExist:
                return super(FCMTokenSerializer, self).is_valid(*args, **kwargs)

    class Meta:
        model = FCMToken
        fields = "__all__"


class FCMTokenUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FCMToken
        fields = ("id", "key")


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')
    fcm_token = FCMTokenSerializer(source="user.fcm_token")
    user = UserSerializer()

    class Meta:
        model = Token
        fields = ("auth_token", "created", "user", "fcm_token")


class PushMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushMessages
        exclude = ("user", )

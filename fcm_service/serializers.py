from rest_framework.exceptions import ValidationError
from rest_framework import serializers, status

from authentication.errors import CustomValidationError
from authentication.models import User
from fcm_service.models import FCMToken, PushMessages


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
                raise CustomValidationError(
                    "key already exists (duplicated key)",
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
            else:
                raise e
        else:

            try:
                fcm_token_exists = self.context.get("request").user.fcm_token
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


class PushMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushMessages
        exclude = ("users", )

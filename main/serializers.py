
from rest_framework import serializers
# from rest_framework.decorators import api_view, permission_classes
from main.choices import ATTACHMENTS_TYPE_CHOICES
from main.models import UserProfile, Attachment#, Notification



class ChoicesSerializerField(serializers.SerializerMethodField):
    """
    A read-only field that return the representation of a model field with choices.
    """

    def to_representation(self, value):
        # sample: 'get_XXXX_display'
        method_name = 'get_{field_name}_display'.format(field_name=self.field_name)
        # retrieve instance method
        method = getattr(value, method_name)
        # finally use instance method to return result of get_XXXX_display()
        return method()

class UserProfileSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = UserProfile
        fields = ["avatar", "user"]


class AttachmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    attachment_type = serializers.CharField(source="get__type_display", read_only=True)

    class Meta:
        model = Attachment
        fields = "__all__"


class AttachmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ("id", "title", "file")


# class NotificationSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Notification
#             fields = '__all__'
#

#
# class PermissionSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Permission
#             fields = '__all__'

# class ClassroomAttchmentSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = ClassroomAttchment
#             fields = '__all__'



#
# class SettingsOptionsSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = SettingsOptions
#             fields = '__all__'
#
#
# class SettingsValuesSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = SettingsValues
#             fields = '__all__'

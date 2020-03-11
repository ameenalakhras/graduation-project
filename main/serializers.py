
from rest_framework import serializers
# from rest_framework.decorators import api_view, permission_classes
from main.models import UserProfile, Attachment#, Notification

soft_delete_fields = ('deleted_at','deleted')


class UserProfileSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = UserProfile
        exclude = soft_delete_fields


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        exclude = soft_delete_fields
        read_only_fields = ('user',)



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

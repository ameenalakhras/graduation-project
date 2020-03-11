
from rest_framework import serializers
# from rest_framework.decorators import api_view, permission_classes
from main.models import UserProfile, Attachment#, Notification

class UserProfileSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = UserProfile
        # fields = '__all__'
        exclude = ('deleted_at','deleted' )


class AttachmentSerializer(serializers.ModelSerializer):
    uploader = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = Attachment
        # fields = '__all__'
        exclude = ('deleted_at','deleted' )



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

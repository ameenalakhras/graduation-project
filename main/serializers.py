
from rest_framework import serializers
# from rest_framework.decorators import api_view, permission_classes
# from reservation.models import  Room, Reserve


class UserProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserProfile
            fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Attachment
            fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Notification
            fields = '__all__'


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

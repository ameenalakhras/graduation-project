from rest_framework import serializers
from course.models import Media



class MediaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Media
            fields = '__all__'

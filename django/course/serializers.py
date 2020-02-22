class MediaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Media
            fields = '__all__'

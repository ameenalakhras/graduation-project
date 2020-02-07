class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = '__all__'

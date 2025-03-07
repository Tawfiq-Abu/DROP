from rest_framework import serializers
from .models import Contestant,UploadedFile

class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = '__all__'

class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = UploadedFile
        fields = ['file']

from rest_framework import serializers
from .models import FileArchive

class FileArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileArchive
        fields = '__all__' 
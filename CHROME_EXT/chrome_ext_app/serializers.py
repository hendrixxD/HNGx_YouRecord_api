from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from .models import *
import uuid


class CreateRecordingSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    class Meta:
        model = Recordings
        fields = ['id', 'name']
        
    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        recordings = Recordings.objects.create(name=uuid.uuid4(), **validated_data)
        return recordings

class GetRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recordings
        fields = ['id', 'name', 'title', 'transcript', 'video', 'created_at']
        
class GetRecordingVideoSerializer(serializers.Serializer):
    recording = GetRecordingSerializer()
    # videos = VideoSerializers(many=True)
    
class TranscriptionSerializer(serializers.ModelSerializer):
    video = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['mp3', 'mp4'])])
    
    class Meta:
        model = Recordings
        fields = ('id', 'title', 'transcript', 'video')


from django.db import models
import os
import uuid

# Create your models here.

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']

class Recordings(TimeStamp):
    title = models.CharField(max_length=300, blank=True, null=True)
    name = models.CharField(max_length=270, blank=True, null=True)
    transcript = models.TextField(blank=True, null=True)
    video = models.FileField(("Video File"), upload_to='videos/', null=True, blank=True)
    is_transcript_completed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    # unique_identifier = models.UUIDField(default=uuid.uuid4, unique=True)
    # size = models.BigIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    # def save(self, *args, **kwargs):
    #    # Automatically set the name from the uploaded video file
    #    if not self.name:
    #        self.name, self.extension = os.path.splitext(os.path.basename(self.recording_data.name))
    #    # automatically set the size of the video file in bytes
    #    if not self.size:
    #        self.size = self.recording_data.size
    #    super(Video, self).save(*args, **kwargs)


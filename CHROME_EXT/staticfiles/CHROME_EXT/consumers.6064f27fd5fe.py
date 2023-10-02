import asyncio
import os
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import HttpResponse
from .models import Video

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        recording_data = text_data.encode()

        # Generate a unique identifier for the video
        unique_identifier = str(uuid.uuid4())

        # Define the file path to save the recording data
        file_path = os.path.join('videos', f'{unique_identifier}.webm')

        # Save the recording data to the disk asynchronously
        await self.save_recording(file_path, recording_data)

        # Save meta data to the database asynchronously
        await self.save_to_database(file_path, unique_identifier)

        # Respond to the client
        await self.send(text_data='Recording data received and saved successfully')

    async def save_recording(self, file_path, recording_data):
        with open(file_path, 'ab') as file:
            file.write(recording_data)

    async def save_to_database(self, file_path, unique_identifier):
        video = await asyncio.to_thread(Video.objects.create,
                                       recording_data=file_path,
                                       unique_identifier=unique_identifier)

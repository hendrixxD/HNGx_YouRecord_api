from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
from moviepy.editor import VideoFileClip, concatenate_videoclips
import tempfile
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_api_payload import error_response, success_response
from rest_framework import generics
from django.http import HttpRequest, HttpResponse
from rest_framework import status
import uuid
from .serializers import CreateRecordingSerializer, GetRecordingSerializer
from .models import Recordings
from rest_framework.views import APIView
from django.http import StreamingHttpResponse
from rest_framework.renderers import JSONRenderer
from django.conf import settings
import os
from django.core.files import File
import io
from django.core.files.base import ContentFile

BASE_URL = 'https://chromeextensionapi-rmrj.onrender.com'

# Create your views here.
BASE_URL = settings.BASE_DIR


class CreateRecordingView(generics.CreateAPIView):
    serializer_class = CreateRecordingSerializer
    queryset = Recordings.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request: HttpRequest):
        serializer = CreateRecordingSerializer(data=request.data)
        name = serializer.initial_data.get("name")
        if serializer.is_valid():
            serializer.save()

            payload = success_response(
                status="success",
                message=f"Recording(s) saved successfully!",
                data=serializer.data
            )
            return Response(data=payload, status=status.HTTP_201_CREATED)
        else:
            payload = error_response(
                status="Failed something went wrong",
                message=serializer.errors
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class AllRecordingsView(generics.ListAPIView):
    serializer_class = GetRecordingSerializer
    queryset = Recordings.objects.all()

    def get(self, request: HttpRequest):

        recordings = self.get_queryset()
        serializers = self.serializer_class(recordings, many=True)
        payload = success_response(
            status="success",
            message=f"All recordings fetched successfully!",
            data=serializers.data
        )
        return Response(data=payload, status=status.HTTP_200_OK)


class GetDataView(APIView):
    def put(self, request, id):
        data = request.data.get("data")
        # print(request.FILES, "request files")
        # print(request.data, "request data")
        recording_id = id
        if recording_id:
            try:
                video = Recordings.objects.get(pk=recording_id)
            except Recordings.DoesNotExist:
                return Response({'error': 'No video found'}, status=status.HTTP_400_BAD_REQUEST)

            if not data:
                return Response({'error': 'No video data provided'}, status=status.HTTP_400_BAD_REQUEST)

            new_video_data = data

            if video.video:
                existing_video_data = video.video.read()
                with tempfile.NamedTemporaryFile(delete=False) as existing_tempfile:
                    existing_tempfile.write(existing_video_data)
                    existing_tempfile_path = existing_tempfile.name

                with tempfile.NamedTemporaryFile(delete=False) as new_tempfile:
                    new_tempfile.write(new_video_data)
                    new_tempfile_path = new_tempfile.name

                existing_clip = VideoFileClip(existing_tempfile_path)
                new_clip = VideoFileClip(new_tempfile_path)

                final_clip = concatenate_videoclips([existing_clip, new_clip])

                with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as final_tempfile:
                    final_clip.write_videofile(
                        final_tempfile.name, codec='libx264')
                    final_tempfile_path = final_tempfile.name

                video.video.save(f'video_{video.id}.mp4', ContentFile(
                    open(final_tempfile_path, 'rb').read()))

                os.remove(existing_tempfile_path)
                os.remove(new_tempfile_path)
                os.remove(final_tempfile_path)

                return Response({'message': 'Video appended and joined successfully'}, status=status.HTTP_200_OK)
            else:
                video.video.save(
                    f'video_{video.id}.webm', new_video_data)
                return Response({'message': 'Video added successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No ID'}, status=status.HTTP_200_OK)


class GetSingleVideoView(generics.ListAPIView):
    serializer_class = GetRecordingSerializer

    def get(self, request:HttpRequest, id:int):
        try:
            video = Recordings.objects.get(id=id)
            serializers = GetRecordingSerializer(video, many=False)
            payload = success_response(
                status="success",
                message=f"Video fetched successfully!",
                data=serializers.data
            )
            return Response(data=payload, status=status.HTTP_200_OK)
        except Recordings.DoesNotExist:
            payload = error_response(
                status="Failed, something went wrong",
                message=f"Video does not exist"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


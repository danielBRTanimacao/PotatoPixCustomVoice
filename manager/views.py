import os

from django.db import transaction
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.files.base import ContentFile

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import InCustomVoiceSerializer, ListCustomVoiceSerializer
from api.models import CustomVoiceModel

from utils.generators import generate_voice
from .task import process_voice_generation

class ManagerCustomVoice(APIView):
    def get(self, request, format=None):
        voice_objs = get_list_or_404(CustomVoiceModel.objects.all())
        voice_serializer = ListCustomVoiceSerializer(voice_objs, many=True)
        return Response(voice_serializer.data)

    @transaction.atomic
    def post(self, request, format=None):
        voice_serializer = InCustomVoiceSerializer(data=request.data)

        if voice_serializer.is_valid(raise_exception=True):
            voice_instance = voice_serializer.save(
                voice_model_file=None,
                status='PENDING'
            )

            sample_audio_file = request.data.get('sample_audio')
            sample_audio_content = sample_audio_file.read()
            file_name = sample_audio_file.name

            process_voice_generation.delay(
                voice_instance.id, 
                sample_audio_content, 
                file_name
            )
            return Response(
                InCustomVoiceSerializer(voice_instance).data, 
                status=status.HTTP_202_ACCEPTED 
            )
        return Response(voice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk: int):
        voice_obj = get_object_or_404(CustomVoiceModel, pk=pk)
        voice_obj_serializer = InCustomVoiceSerializer(voice_obj, data=request.data)
        
        if voice_obj_serializer.is_valid(raise_exception=True):
            generated_file = generate_voice(request.data.get('sample_audio'))
            voice_obj_serializer.save(voice_model_file=generated_file)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(voice_obj_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    def delete(self, request, pk: int):
        voice_obj = get_object_or_404(CustomVoiceModel, pk=pk)
        voice_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
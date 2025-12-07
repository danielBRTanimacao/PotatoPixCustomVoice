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

class ManagerCustomVoice(APIView):
    def get(self, request, format=None):
        voice_objs = get_list_or_404(CustomVoiceModel.objects.all())
        voice_serializer = ListCustomVoiceSerializer(voice_objs, many=True)
        return Response(voice_serializer.data)

    @transaction.atomic
    def post(self, request, format=None):
        voice_serializer = InCustomVoiceSerializer(data=request.data)
        temp_audio = None 

        if voice_serializer.is_valid(raise_exception=True):
            reference_audio = request.data.get('sample_audio')

            if not reference_audio:
                return Response({"detail": "Path to audio reference is invalid"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                temp_audio = generate_voice(reference_audio)

                with open(temp_audio, 'rb') as file:
                    audio_content = ContentFile(file.read())

                    voice_serializer.sample_audio.save(
                        name=os.path.basename(temp_audio),
                        content=audio_content,
                        save=False 
                    )
                voice_serializer.save()
                
                return Response(status.HTTP_201_CREATED)
                
            except Exception as ex:
                return Response({"detail": f"Internal error cannot generate or save the audio: {ex}"}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            finally:
                if temp_audio and os.path.exists(temp_audio):
                    os.remove(temp_audio)
        return Response(voice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        voice_obj = CustomVoiceModel.objects.get(pk=pk)
        voice_obj_serializer = InCustomVoiceSerializer(voice_obj, data=request.data)
        if voice_obj_serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(voice_obj_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    def delete(self, pk: int, request):
        voice_obj = get_object_or_404(CustomVoiceModel.objects.get(pk=pk))
        voice_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
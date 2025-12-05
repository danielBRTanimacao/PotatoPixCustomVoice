from django.shortcuts import get_list_or_404

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import InCustomVoiceSerializer, ListCustomVoiceSerializer
from api.models import CustomVoiceModel

class ManagerCustomVoice(APIView):
    def get(self, request, format=None):
        voice_objs = get_list_or_404(CustomVoiceModel.objects.all())
        voice_serializer = ListCustomVoiceSerializer(voice_objs, many=True)
        return Response(voice_serializer.data)

    def post(self, request, format=None):
        voice_serializer = InCustomVoiceSerializer(data=request.data)
        if voice_serializer.is_valid(raise_exception=True):
            # generator
            voice_serializer.save()
            return Response(status.HTTP_201_CREATED)
        return Response(voice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
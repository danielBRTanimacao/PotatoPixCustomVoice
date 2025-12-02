import os

from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from dotenv import load_dotenv

from .models import CustomVoiceModel

load_dotenv()

WEBHOOK_JAVA_SECRET = os.getenv('WEBHOOK_JAVA_SECRET')
BACKEND_SECRET = os.getenv('BACKEND_SECRET')

@api_view(["POST"])
def submit_voice(request):
    if WEBHOOK_JAVA_SECRET != request.GET.get('websecret') or BACKEND_SECRET != request.headers.get('x-backend-secret'):
        return Response("unauthorized websecret or header is invalid", status=status.HTTP_401_UNAUTHORIZED)

    name_to_find = request.POST.get('name')
    if not name_to_find:
        return Response({"detail": "field 'name' is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        voice_obj = get_object_or_404(CustomVoiceModel, name__icontains=name_to_find)
    except ValueError as e:
        return Response({"detail": f"Err to find obj: {e}"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response()

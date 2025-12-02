import os

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from dotenv import load_dotenv

load_dotenv()

WEBHOOK_JAVA_SECRET = os.getenv('WEBHOOK_JAVA_SECRET')
BACKEND_SECRET = os.getenv('BACKEND_SECRET')

@api_view(["POST"])
def submit_voice(request):
    if WEBHOOK_JAVA_SECRET != request.GET.get('websecret') or BACKEND_SECRET != request.headers.get('x-backend-secret'):
        return Response("unauthorized websecret or header is invalid", status=status.HTTP_401_UNAUTHORIZED)

    return Response()

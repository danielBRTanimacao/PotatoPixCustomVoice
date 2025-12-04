from rest_framework.decorators import api_view

@api_view(['GET'])
def list_all_voices(request):
    ...
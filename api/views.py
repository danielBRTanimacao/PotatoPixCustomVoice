from ninja import NinjaAPI
from ninja.responses import Response

api = NinjaAPI()

@api.get('')
def get_all_voices(request):
    return Response({'data': 'data'})

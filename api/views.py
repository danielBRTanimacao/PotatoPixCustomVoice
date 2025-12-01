import os

from ninja import NinjaAPI
from ninja.responses import Response
from ninja.errors import HttpError

from dotenv import load_dotenv

api = NinjaAPI()
load_dotenv()

WEBHOOK_JAVA_SECRET = os.getenv('WEBHOOK_JAVA_SECRET')
BACKEND_SECRET = os.getenv('BACKEND_SECRET') # passar o HEader depois

@api.get('voices')
def submit_voice(request, websecret: str):
    if WEBHOOK_JAVA_SECRET != websecret:
        print(WEBHOOK_JAVA_SECRET)
        raise HttpError(401, "unauthorized websecret is invalid")
    
    return Response({'data': websecret})

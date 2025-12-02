from rest_framework.serializers import ModelSerializer

from .models import CustomVoiceModel

class CustomVoiceSerializer(ModelSerializer):
    class Meta:
        model = CustomVoiceModel
        fields = "name",
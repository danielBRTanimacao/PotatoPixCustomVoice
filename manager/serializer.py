from rest_framework.serializers import ModelSerializer, Serializer

from .models import CustomVoiceModel

class InCustomVoiceSerializer(ModelSerializer):
    class Meta:
        model = CustomVoiceModel
        fields = "name", "voice_model_file", "sample_audio",

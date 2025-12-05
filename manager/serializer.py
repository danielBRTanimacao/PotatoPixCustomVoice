from rest_framework.serializers import ModelSerializer, Serializer

from api.models import CustomVoiceModel

class InCustomVoiceSerializer(ModelSerializer):
    class Meta:
        model = CustomVoiceModel
        fields = "name", "sample_audio",

class ListCustomVoiceSerializer(ModelSerializer):
    class Meta:
        model = CustomVoiceModel
        fields = "__all__"

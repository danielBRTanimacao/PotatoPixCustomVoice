from celery import shared_task
from django.core.files.base import ContentFile
import os
import tempfile
import numpy
import soundfile
from TTS.api import TTS
import torch

from api.models import CustomVoiceModel 

TTS_MODEL_INSTANCE = None 

def load_tts_model():
    """Carrega o modelo TTS uma única vez por worker do Celery."""
    global TTS_MODEL_INSTANCE
    if TTS_MODEL_INSTANCE is None:
        DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Carregando modelo XTTS-v2 no dispositivo: {DEVICE}")
        TTS_MODEL_INSTANCE = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(DEVICE)
    return TTS_MODEL_INSTANCE


@shared_task
def process_voice_generation(voice_instance_id: int, sample_audio_content: bytes, file_name: str):
    """
        Gera as vozes em segundo plano.
    """
    LANG = 'pt'
    MSG = "Use a minha voz para enviar essa mensagem!"
    tts = load_tts_model()

    temp_in_path = None
    temp_out_path = None
    
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_in:
            temp_in.write(sample_audio_content)
            temp_in_path = temp_in.name

        audio = tts.tts(
            text=MSG,
            speaker_wav=temp_in_path,
            language=LANG,
            speed=1.0,
        )

        audio_array = numpy.array(audio, dtype=numpy.float32)
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_out:
            temp_out_path = temp_out.name
        
        soundfile.write(temp_out_path, audio_array, samplerate=22050, format="ogg")
        voice_instance = CustomVoiceModel.objects.get(pk=voice_instance_id)
        
        with open(temp_out_path, 'rb') as f:
            file_content = ContentFile(f.read())
            voice_instance.voice_model_file.save(f'{voice_instance.name}_model.ogg', file_content) 
        
        voice_instance.status = 'COMPLETED'
        voice_instance.save()

    except Exception as e:
        print(f"Erro na geração de voz para a instância {voice_instance_id}: {e}")
        try:
             voice_instance = CustomVoiceModel.objects.get(pk=voice_instance_id)
             voice_instance.status = 'FAILED'
             voice_instance.save()
        except Exception as update_err:
             print(f"Erro ao atualizar status para FAILED: {update_err}")

    finally:
        if temp_in_path and os.path.exists(temp_in_path):
            os.remove(temp_in_path)
        if temp_out_path and os.path.exists(temp_out_path):
            os.remove(temp_out_path)
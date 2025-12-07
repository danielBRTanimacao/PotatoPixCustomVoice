import torch
from TTS.api import TTS
import soundfile
import tempfile
import numpy

def generate_voice(voice_file) -> str:
    LANG = 'pt'
    MSG = "Use a minha voz para enviar essa mensagem!"
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_in:
        for chunk in voice_file.chunks():
            temp_in.write(chunk)
        temp_in_path = temp_in.name

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(DEVICE)

    audio = tts.tts(
        text=MSG,
        speaker_wav=temp_in_path,
        language=LANG,
        speed=1.0,
    )

    audio_array = numpy.array(audio, dtype=numpy.float32)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_out:
        temp_out_path = temp_out.name

    soundfile.write(temp_out_path, audio_array, samplerate=22050, format="mp3")
    return temp_out_path
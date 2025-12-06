import torch
from TTS.api import TTS
import soundfile
import tempfile
import numpy

def generate_voice(voice: str) -> str:
    LANG = 'pt'
    MSG = "Use a minha voz para enviar essa mensagem!"
    DEVICE = 'cpu'

    if torch.cuda.is_available():
        DEVICE = 'cuda'

    tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2').to(DEVICE)

    audio = tts.tts(
        text=MSG,
        speaker_wav=str(voice),
        language=LANG,
        speed=1.0,
        enable_text_splitting=False,
        temperature=0.1, 
        gpt_cond_len=5,
        gpt_cond_chunk_len=5,
    )

    audio_array = numpy.array(audio, dtype=numpy.float32)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
        temp_path = temp.name

    soundfile.write(temp_path, audio_array, samplerate=22050, format="mp3")
    return temp_path

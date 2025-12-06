from pathlib import Path

import torch
from TTS.api import TTS
import soundfile
import numpy

BASE_DIR = Path(__file__).resolve().parent

VOICE_DIR = BASE_DIR / 'voices'
#VOICE_FILE = VOICE_DIR / 'bobEsponja.wav'
VOICE_FILE = VOICE_DIR / 'silvioSantos.wav'

def generate_voice(voice: str) -> None:
    OUTPUT_PATH = BASE_DIR / "output.mp3"

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

    soundfile.write(OUTPUT_PATH, audio_array, samplerate=22050, format="mp3")

generate_voice(VOICE_FILE)
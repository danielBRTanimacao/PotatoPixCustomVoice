from pathlib import Path

import torch
from TTS.api import TTS
from tempfile import NamedTemporaryFile
import numpy
import io
import soundfile

BASE_DIR = Path(__file__).resolve().parent

VOICE_DIR = BASE_DIR / 'voices'
VOICE_FILE = VOICE_DIR / 'bobEsponja.wav'
LANG = 'pt'
MSG = "Iae meu nobre, como vai?"
DEVICE = 'cpu'

if torch.cuda.is_available():
    DEVICE = 'cuda'

tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2').to(DEVICE)

with NamedTemporaryFile(dir=VOICE_DIR, suffix='.mp3') as voice:
    voice.write(VOICE_FILE.file.read())
    voice_path = voice.name
    
    speech_file = tts.tts(
        text=MSG,
        speaker_mp3=voice_path,
        language=LANG
    )

audio_array = numpy.array(speech_file, dtype=numpy.float32)

audio_stream= io.BytesIO()
soundfile.write(audio_stream, audio_array, samplerate=22050, format='mp3')
audio_stream.seek(0)
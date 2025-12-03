"""
# usar uma voz de base (obrigatorio)
# ter uma mensagem (obrigatorio)
# uma linguagem tipo (pt, en, es e etc)
# se vai ser CPU ou GPU para rodar a aplicação
# salvar o model com o audio gerado e a prerenderização para testes
"""

from pathlib import Path

import torch
import pyttsx3
from tempfile import NamedTemporaryFile

BASE_DIR = Path(__file__).resolve().parent

VOICE_DIR = BASE_DIR / 'voices'
MSG = "Iae meu nobre, como vai?"

engine = pyttsx3.init()

with NamedTemporaryFile(dir=VOICE_DIR, suffix='.mp3') as voice:
    # gerar a voz
    # salvar
    ...
import torch

x = torch.rand(5, 3)
print(x)

print(torch.cuda.is_available()) # CUDA ta desativado mas acho que com CPU da pra clonar a voz

# ========== ACho que vai ser necessario ==============
# Usar o tts Text to speach para transfomrar o texto em audio torch combinado para machine learning
# usar uma voz de base (obrigatorio)
# ter uma mensagem (obrigatorio)
# uma linguagem tipo (pt, en, es e etc)
# se vai ser CPU ou GPU para rodar a aplicação
# salvar o model com o audio gerado e a prerenderização para testes
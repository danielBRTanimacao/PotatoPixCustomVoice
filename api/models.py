from django.db import models

class CustomVoiceModel(models.Model):
    class Meta:
        verbose_name = "Personal Voz Model"
        verbose_name_plural = "Modelos de Voz Personalizadas"

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100, unique=True)
    
    voice_model_file = models.FileField(
        upload_to='voice_models/',
        verbose_name="Model Voz file (IA)",
        help_text="The file is binary and permanent, model Ia learned (.pth, .pt, .zip)"
    )

    sample_audio = models.FileField(
        upload_to='sample_audios/',
        blank=True,
        null=True,
        verbose_name="Original audio sample",
        help_text="Reference audio (ogg/mp3) used to train or demonstration."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
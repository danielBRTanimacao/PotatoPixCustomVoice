from django.db import models

class CustomVoiceModel(models.Model):
    name = models.CharField(max_length=100)
    # ogg audio
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    '''
    /api/voices?webhooktoken=123
    backend_java_token=321
    {
        'voice': 'Bob esponja',
        'msg': "Fulano mandou 10 conto. Bom dia como vai!"
    }

    PYTHON_WEBHOOK_KEY=123
    PYTHON_BACKEND=321
    '''
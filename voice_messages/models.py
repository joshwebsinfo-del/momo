import uuid

from django.conf import settings
from django.db import models


class VoiceMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_voice_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_voice_messages')
    audio = models.FileField(upload_to='voice-notes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Voice message from {self.sender}'

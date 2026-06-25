"""voice_messages/models.py — Voice message model."""
import uuid
from django.db import models
from django.conf import settings


class VoiceMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_voice_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_voice_messages'
    )
    title = models.CharField(max_length=200, blank=True, default='Voice Message')
    audio_url = models.URLField(help_text='Supabase Storage URL')
    duration_seconds = models.PositiveIntegerField(default=0)
    is_listened = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'voice_message'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} — {self.sender} → {self.receiver}'

    @property
    def duration_display(self):
        minutes = self.duration_seconds // 60
        seconds = self.duration_seconds % 60
        return f'{minutes}:{seconds:02d}'

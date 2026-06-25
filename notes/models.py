"""notes/models.py — LoveNote with future delivery support."""
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class LoveNote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notes'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_notes'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()  # Rich text HTML stored here
    scheduled_for = models.DateTimeField(
        null=True, blank=True,
        help_text='If set, the note will not be visible until this datetime.'
    )
    is_delivered = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notes_lovenote'
        ordering = ['-created_at']
        verbose_name = 'Love Note'

    def __str__(self):
        return f'{self.title} — {self.sender} → {self.receiver}'

    def save(self, *args, **kwargs):
        # If no scheduled time set, deliver immediately
        if not self.scheduled_for:
            self.is_delivered = True
        elif self.scheduled_for <= timezone.now():
            self.is_delivered = True
        super().save(*args, **kwargs)

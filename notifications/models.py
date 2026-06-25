"""notifications/models.py — Notification model."""
import uuid
from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPES = [
        ('note', 'New Love Note'),
        ('goal', 'Goal Milestone'),
        ('countdown', 'Countdown Alert'),
        ('anniversary', 'Anniversary'),
        ('voice', 'Voice Message'),
        ('memory', 'New Memory'),
        ('general', 'General'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPES, default='general')
    link = models.CharField(max_length=500, blank=True, default='')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications_notification'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} → {self.user}'

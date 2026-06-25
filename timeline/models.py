"""timeline/models.py — TimelineEvent model."""
import uuid
from django.db import models


class TimelineEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    image_url = models.URLField(blank=True, default='')
    event_date = models.DateField()
    event_icon = models.CharField(
        max_length=10, default='❤️',
        help_text='Emoji icon for this event'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'timeline_event'
        ordering = ['event_date']
        verbose_name = 'Timeline Event'

    def __str__(self):
        return f'{self.title} ({self.event_date})'

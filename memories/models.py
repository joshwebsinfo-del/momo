"""memories/models.py — Memory model with Supabase Storage URLs."""
import uuid
from django.db import models
from django.conf import settings


class Memory(models.Model):
    CATEGORY_CHOICES = [
        ('date', 'Date'),
        ('trip', 'Trip'),
        ('anniversary', 'Anniversary'),
        ('birthday', 'Birthday'),
        ('random', 'Random Moment'),
        ('achievement', 'Achievement'),
        ('first', 'A First'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    photo_url = models.URLField(blank=True, default='', help_text='Supabase Storage URL')
    video_url = models.URLField(blank=True, default='', help_text='Supabase Storage URL')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='random')
    memory_date = models.DateField()
    location = models.CharField(max_length=200, blank=True, default='')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='memories'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'memories_memory'
        ordering = ['-memory_date']
        verbose_name = 'Memory'
        verbose_name_plural = 'Memories'

    def __str__(self):
        return f'{self.title} ({self.memory_date})'

    @property
    def has_media(self):
        return bool(self.photo_url or self.video_url)

    @property
    def media_type(self):
        if self.video_url:
            return 'video'
        if self.photo_url:
            return 'photo'
        return 'none'

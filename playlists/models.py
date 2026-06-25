"""playlists/models.py — Relationship songs playlist."""
import uuid
from django.db import models
from django.conf import settings


class Song(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    youtube_url = models.URLField(help_text='Full YouTube video URL')
    memory_description = models.TextField(
        blank=True, default='',
        help_text='Why does this song matter to your relationship?'
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='songs'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'playlists_song'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} — {self.artist}'

    @property
    def youtube_embed_url(self):
        """Convert YouTube watch URL to embed URL."""
        url = self.youtube_url
        if 'watch?v=' in url:
            video_id = url.split('watch?v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        return url  # Already an embed URL

    @property
    def youtube_thumbnail(self):
        url = self.youtube_url
        video_id = None
        if 'watch?v=' in url:
            video_id = url.split('watch?v=')[1].split('&')[0]
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
        if video_id:
            return f'https://img.youtube.com/vi/{video_id}/hqdefault.jpg'
        return ''

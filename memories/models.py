import uuid

from django.conf import settings
from django.db import models


class Memory(models.Model):
    CATEGORY_CHOICES = [
        ('Date', 'Date'),
        ('Trip', 'Trip'),
        ('Anniversary', 'Anniversary'),
        ('Birthday', 'Birthday'),
        ('Random Moment', 'Random Moment'),
        ('Achievement', 'Achievement'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='memories/photos/', blank=True, null=True)
    video = models.FileField(upload_to='memories/videos/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Random Moment')
    memory_date = models.DateField()
    location = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MemoryComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    memory = models.ForeignKey(Memory, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} on {self.memory}'

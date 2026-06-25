import uuid

from django.conf import settings
from django.db import models


class DailyCheckIn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='checkins')
    check_in_date = models.DateField(unique=True)
    mood = models.CharField(max_length=50, blank=True)
    note = models.TextField(blank=True)
    gratitude = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-check_in_date']

    def __str__(self):
        return f'{self.user} - {self.check_in_date}'

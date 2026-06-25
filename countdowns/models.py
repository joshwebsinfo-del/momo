"""countdowns/models.py — Countdown events."""
import uuid
from django.db import models
from django.utils import timezone


class Countdown(models.Model):
    COUNTDOWN_TYPES = [
        ('anniversary', 'Anniversary'),
        ('birthday', 'Birthday'),
        ('trip', 'Trip / Vacation'),
        ('graduation', 'Graduation'),
        ('wedding', 'Wedding'),
        ('custom', 'Custom Event'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    target_date = models.DateField()
    countdown_type = models.CharField(max_length=20, choices=COUNTDOWN_TYPES, default='custom')
    is_recurring_yearly = models.BooleanField(
        default=False,
        help_text='If true, automatically resets each year (e.g., anniversaries)'
    )
    cover_emoji = models.CharField(max_length=10, default='🎉')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'countdowns_countdown'
        ordering = ['target_date']

    def __str__(self):
        return self.title

    @property
    def days_remaining(self):
        today = timezone.now().date()
        delta = self.target_date - today
        return delta.days

    @property
    def is_past(self):
        return self.days_remaining < 0

    @property
    def is_today(self):
        return self.days_remaining == 0

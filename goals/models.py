import uuid

from django.conf import settings
from django.db import models

from reminders.models import Reminder


class Goal(models.Model):
    TYPE_CHOICES = [
        ('Savings', 'Savings'),
        ('Travel', 'Travel'),
        ('Personal', 'Personal'),
        ('Business', 'Business'),
        ('Education', 'Education'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    target_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    goal_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Savings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def percent_complete(self):
        if self.target_amount <= 0:
            return 0
        return min(100, int((self.current_amount / self.target_amount) * 100))

    def __str__(self):
        return self.title

    def create_goal_reminder(self):
        if not self.target_date:
            return None
        return Reminder.objects.get_or_create(
            user=self.user,
            title=f'Goal deadline: {self.title}',
            reminder_date=self.target_date,
            defaults={'note': f'Keep working on your goal: {self.title}', 'is_done': False},
        )

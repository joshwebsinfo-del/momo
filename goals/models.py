"""goals/models.py — Savings and relationship goal tracking."""
import uuid
from django.db import models
from django.utils import timezone


class Goal(models.Model):
    GOAL_TYPES = [
        ('savings', 'Savings'),
        ('travel', 'Travel'),
        ('personal', 'Personal'),
        ('business', 'Business'),
        ('education', 'Education'),
        ('home', 'Home'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES, default='savings')
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    target_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    cover_image_url = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goals_goal'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def progress_percent(self):
        if self.target_amount <= 0:
            return 0
        pct = (self.current_amount / self.target_amount) * 100
        return min(int(pct), 100)

    @property
    def remaining_amount(self):
        return max(self.target_amount - self.current_amount, 0)

    def save(self, *args, **kwargs):
        if self.current_amount >= self.target_amount and not self.completed:
            self.completed = True
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)


class GoalContribution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.CharField(max_length=300, blank=True, default='')
    contributed_at = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'goals_contribution'
        ordering = ['-contributed_at']

    def __str__(self):
        return f'+{self.amount} → {self.goal.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update goal's current amount
        from django.db.models import Sum
        total = self.goal.contributions.aggregate(total=Sum('amount'))['total'] or 0
        self.goal.current_amount = total
        self.goal.save(update_fields=['current_amount', 'completed', 'completed_at'])

"""goals/signals.py — Notify when a goal is completed."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Goal


@receiver(post_save, sender=Goal)
def notify_goal_completed(sender, instance, **kwargs):
    """Fire a notification to both users when a goal reaches 100%."""
    if instance.completed:
        from notifications.models import Notification
        from django.contrib.auth import get_user_model
        User = get_user_model()
        for user in User.objects.all():
            # Avoid duplicate notifications
            already = Notification.objects.filter(
                user=user,
                link=f'/goals/{instance.pk}/',
                notification_type='goal',
            ).exists()
            if not already:
                Notification.objects.create(
                    user=user,
                    title='🎉 Goal Achieved!',
                    message=f'You reached your goal: "{instance.title}"! Congratulations!',
                    notification_type='goal',
                    link=f'/goals/{instance.pk}/',
                )

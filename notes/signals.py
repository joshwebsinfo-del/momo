"""notes/signals.py — Notify receiver when a note is delivered."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LoveNote


@receiver(post_save, sender=LoveNote)
def notify_on_delivery(sender, instance, created, **kwargs):
    if created and instance.is_delivered:
        from notifications.models import Notification
        Notification.objects.create(
            user=instance.receiver,
            title='💌 New Love Note',
            message=f'{instance.sender.display_name} sent you a note: "{instance.title}"',
            notification_type='note',
            link=f'/notes/{instance.pk}/',
        )
